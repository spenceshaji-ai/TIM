from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

class Role(models.Model):
     role_name = models.CharField(max_length=50)
     description = models.TextField(blank=True, null=True)

     def __str__(self):
         return self.role_name
     
class User(AbstractUser):
     name = models.CharField(max_length=255)
     phone_number = models.CharField(
     max_length=15,
     unique=True,
     null=True,
     blank=True
     )
     role = models.ForeignKey(
     Role,
     on_delete=models.SET_NULL,  
     null=True,
     blank=True
    )

     STATUS_CHOICES = (
         ("active", "Active"),
         ("inactive", "Inactive"),
     )

     status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active"
     )

     def __str__(self):
    # Shows full name if available, else username
      return self.name if self.name else self.username
