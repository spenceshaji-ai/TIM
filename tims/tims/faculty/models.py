from django.db import models
from tims.adminapp.models import Batch
from django.conf import settings
from django.utils import timezone
# Create your models here.

class TrainingSession(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    faculty = models.ForeignKey("users.User", on_delete=models.CASCADE)
    session_date = models.DateField()
    topic_covered = models.TextField()
    hours_taken = models.DecimalField(max_digits=4, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['batch', 'session_date'],
                name='unique_batch_session_date'
            )
        ]

    def __str__(self):
        return f"{self.batch} - {self.session_date}"     


class StudentAttendance(models.Model):
    student = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='attendance_as_student')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    faculty = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='attendance_as_faculty')

    attendance_date = models.DateField()
    is_present = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'attendance_date')

    def __str__(self):
        return f"{self.student} - {self.attendance_date}"        


class FacultyDailyReport(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="daily_reports")
    report_date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    activities = models.TextField()
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('faculty', 'report_date', 'start_time')
        ordering = ['-report_date']
    def __str__(self):
        return f"{self.faculty} - {self.report_date} ({self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')})"    
from tims.users.models import User
from tims.adminapp.models import Course, Batch


class FacultyCourseMaterial(models.Model):
    MATERIAL_TYPE = (
        ("pdf", "PDF"),
        ("image", "Image"),
        ("video", "Video"),
    )

    faculty = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role__role_name": "faculty"},
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    material_type = models.CharField(
        max_length=10,
        choices=MATERIAL_TYPE
    )

    pdf_file = models.FileField(
        upload_to="faculty/materials/pdfs/",
        blank=True,
        null=True
    )
    image_file = models.ImageField(
        upload_to="faculty/materials/images/",
        blank=True,
        null=True
    )
    video_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course} ({self.batch})"

class BatchCompletionRequest(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="batch_completion_requests"
    )
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="completion_requests"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="completion_requests"
    )

    requested_completion_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    admin_remarks = models.TextField(blank=True, null=True)

    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.batch.batch_name} - {self.faculty} - {self.status}"