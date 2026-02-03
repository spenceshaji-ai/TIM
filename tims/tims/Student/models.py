from django.db import models
from Admin.models import Job   

class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    # Foreign Key
    course = models.ForeignKey(
        "adminapp.Course",
        on_delete=models.CASCADE,
        related_name='students'
    )

    passout_year = models.IntegerField()
    qualification = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

from django.db import models

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    # ✅ ForeignKey to Student
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    # ✅ Resume upload
    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_date = models.DateField()

    def __str__(self):
        return f"{self.job.title} - {self.student.name}"

