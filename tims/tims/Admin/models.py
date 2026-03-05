from django.db import models

class Jobtype(models.Model):
    job_type = models.CharField(max_length=100)

    def __str__(self):
        return self.job_type


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.ForeignKey(Jobtype, on_delete=models.CASCADE)
    salary = models.CharField(max_length=100)

    application_deadline = models.DateField()
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Interview(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    application = models.OneToOneField(
        'Student.JobApplication',
        on_delete=models.CASCADE,
        related_name='interview'
    )
    interview_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    feedback = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application.student.name} - {self.interview_date.strftime('%Y-%m-%d %H:%M')}"
