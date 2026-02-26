from django.db import models
from tims.users.models import User



from django.conf import settings
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


class Enquiry(models.Model):

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15,unique=True)
    email = models.EmailField(blank=True, null=True)

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE
    )

    source = models.CharField(
        max_length=20,
        choices=[
            ("Call", "Call"),
            ("Website", "Website"),
            ("Walk-in", "Walk-in"),
            ("Reference", "Reference"),
        ]
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("New", "New"),
            ("Contacted", "Contacted"),
            ("Converted", "Converted"),
            ("Not Interested", "Not Interested"),
            ("Closed", "Closed"),

        ],
        default="New"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    next_followup_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.course_name}"
    
class FollowUp(models.Model):

    enquiry = models.ForeignKey(
        Enquiry,
        on_delete=models.CASCADE,
        related_name="followups"
    )
    today_remark = models.TextField(blank=True, null=True)    # today's discussion
    followup_date = models.DateField()
    next_followup_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Missed", "Missed"),
        ],
        default="Pending"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.enquiry.name} - {self.followup_date}"

class Admission(models.Model):

    enquiry = models.OneToOneField(
        Enquiry,
        on_delete=models.CASCADE,
        related_name="admission"
    )

    admission_date = models.DateField(auto_now_add=True)

    student_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    batch = models.ForeignKey(
        "Batch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=50,
        default="Admitted"
    )

    def __str__(self):
        return self.student_name
    


class Payment(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )

    admission = models.ForeignKey(
        Admission,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.admission.student_name} - {self.amount}"



from django.db import models
from django.core.exceptions import ValidationError

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


