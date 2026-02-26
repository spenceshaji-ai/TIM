from django.db import models
<<<<<<< Updated upstream
from django.conf import settings
=======

>>>>>>> Stashed changes


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    course = models.ForeignKey(
        'adminapp.Course',
        on_delete=models.CASCADE,
        related_name='students',
    )

    passout_year = models.IntegerField()
    qualification = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview', 'Interview'),
    ]

    
    job = models.ForeignKey(
        'Admin.Job',
        on_delete=models.CASCADE,
        related_name='applications'
    )

    student = models.ForeignKey(
        'Student.Student',
        on_delete=models.CASCADE,
        related_name='applications'
    )

    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.job.title} - {self.student.name}"

