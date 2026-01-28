from django.db import models

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    syllabus = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return self.course_name

class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Role, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.batch_name
