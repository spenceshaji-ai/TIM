from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for TIMS.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

from django.db import models

class TrainingSession(models.Model):
    STATUS_CHOICES = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )

    APPROVAL_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

   # batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    #faculty = models.ForeignKey(Role, on_delete=models.CASCADE)
    session_date = models.DateField()
    topic_covered = models.TextField()
    hours_taken = models.DecimalField(max_digits=4, decimal_places=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.batch} - {self.session_date}"    


class StudentAttendance(models.Model):
    ATTENDANCE_STATUS = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
)

    #student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    #faculty = models.ForeignKey('faculty.Faculty', on_delete=models.CASCADE)
    #batch = models.ForeignKey('batches.Batch', on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=ATTENDANCE_STATUS,
        default='Present'
    )
    #class Meta:
       # unique_together = ('student', 'attendance_date')

    def __str__(self):
        return f"{self.student} - {self.attendance_date} - {self.status}"
