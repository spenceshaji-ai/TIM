from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone



# Role Table    
class Role(models.Model):
    role_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.role_name
 
# ✅ Only ONE User Table
class User(AbstractUser):

    # Extra field already in your project
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    # ✅ Your required fields
    phone = models.CharField(max_length=15, blank=True, null=True)

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Active"
    )

    created_at = models.DateTimeField(default=timezone.now)

    # Remove first_name and last_name
    first_name = None
    last_name = None

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


