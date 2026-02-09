from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
User = get_user_model()


class LeaveType(models.Model):
    leave_name = models.CharField(max_length=50)
    max_days = models.PositiveIntegerField()

    def __str__(self):
        return self.leave_name


class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending"
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user} - {self.leave_type}"
# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    syllabus = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.course_name

class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=100) 
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.batch_name



class FacultyAssignment(models.Model):
    faculty = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey("adminapp.Course", on_delete=models.CASCADE)
    batch = models.ForeignKey("adminapp.Batch", on_delete=models.CASCADE)

    class Meta:
        # Enforce that each faculty can only have one assignment per course & batch
        constraints = [
            models.UniqueConstraint(
                fields=["faculty", "course", "batch"],
                name="unique_faculty_course_batch_per_faculty"
            )
        ]

    def __str__(self):
        return f"{self.faculty} - {self.course} - {self.batch}"

    def clean(self):
        """
        Prevent duplicates for the same faculty.
        Different faculties can have same course & batch.
        """
        if FacultyAssignment.objects.filter(
            faculty=self.faculty,
            course=self.course,
            batch=self.batch
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"{self.faculty} is already assigned to this course and batch."
            )

    def save(self, *args, **kwargs):
        self.clean()  # enforce validation
        super().save(*args, **kwargs)


class Assignstudent(models.Model):    
    student = models.ForeignKey("users.User", on_delete=models.CASCADE)  
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.course} ({self.batch})"


