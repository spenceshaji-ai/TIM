from django.db import models
from adminapp.models import Batch
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
