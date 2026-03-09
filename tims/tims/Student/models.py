from django.db import models
from django.conf import settings

from django.utils import timezone

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

class Feedback(models.Model):
    certificate = models.OneToOneField(
        "adminapp.Certificate",
        on_delete=models.CASCADE,
        related_name="feedback"
    )
    rating_choices = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 stars
    rating = models.PositiveSmallIntegerField(choices=rating_choices)
    comment = models.TextField(blank=True)
    submitted_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback by {self.certificate.student.student.name} for {self.certificate.student.course.course_name}"

