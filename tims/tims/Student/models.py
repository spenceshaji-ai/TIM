from django.db import models
from django.conf import settings


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    course = models.ForeignKey(
        "adminapp.Course",
        on_delete=models.CASCADE,
    )

    passout_year = models.IntegerField()
    qualification = models.CharField(max_length=100)

    def __str__(self):   
        return self.name
    

