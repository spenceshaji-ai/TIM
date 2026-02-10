from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from adminapp.models import Course


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



class Enquiry(models.Model):
    """
    Enquiry Table (Handled by Staff Users)
    course_id is Foreign Key → Course Table
    """

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    # ✅ Foreign Key: course_id (Interested Course)
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    source = models.CharField(
        max_length=20,
        choices=[
            ("Call", "Call"),
            ("Website", "Website"),
            ("Walk-in", "Walk-in"),
            ("Reference", "Reference"),
        ]
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("New", "New"),
            ("Contacted", "Contacted"),
            ("Converted", "Converted"),
            ("Closed", "Closed"),
        ],
        default="New"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.course_name}"
