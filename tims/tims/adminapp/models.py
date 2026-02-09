from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LeaveType(models.Model):
    leave_name = models.CharField(max_length=50)
    max_days = models.PositiveIntegerField()

    def __str__(self):
        return self.leave_name


class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending"
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user} - {self.leave_type}"
