from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=100)   # Full-time / Internship
    salary = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    


