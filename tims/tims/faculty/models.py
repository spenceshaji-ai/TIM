from django.db import models
from adminapp.models import Batch

# Create your models here.

class TrainingSession(models.Model):
    STATUS_CHOICES = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    faculty = models.ForeignKey("users.User", on_delete=models.CASCADE)
    session_date = models.DateField()
    topic_covered = models.TextField()
    hours_taken = models.DecimalField(max_digits=4, decimal_places=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    approval_status = models.CharField(max_length=20,default='Pending')

    def __str__(self):
        return f"{self.batch} - {self.session_date}"    


class StudentAttendance(models.Model):
    ATTENDANCE_STATUS = (('Present', 'Present'), ('Absent', 'Absent'))

    student = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='attendance_as_student')
    faculty = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='attendance_as_faculty')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS, default='Present')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'attendance_date'], name='unique_student_attendance_per_day')
        ]

    def __str__(self):
        return f"{self.student} - {self.attendance_date} - {self.status}"


