from django.db import models

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

#class FacultyAssignment(models.Model):
   # faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    #course = models.ForeignKey(Course, on_delete=models.CASCADE)
  #  batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    #def __str__(self):
        #return f"{self.faculty} - {self.course} - {self.batch}"
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return f"{self.user} - {self.leave_type}"
