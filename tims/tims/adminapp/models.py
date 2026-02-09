from django.db import models
from tims.users.models import User



# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    syllabus = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.course_name

class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey( "users.Role", on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.batch_name


class Enquiry(models.Model):

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    course = models.ForeignKey(
        "Course",
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

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.course_name}"
    
class FollowUp(models.Model):

    enquiry = models.ForeignKey(
        Enquiry,
        on_delete=models.CASCADE,
        related_name="followups"
    )

    followup_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Missed", "Missed"),
        ],
        default="Pending"
    )

    remarks = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enquiry.name} - {self.followup_date}"

class Admission(models.Model):

    enquiry = models.OneToOneField(
        Enquiry,
        on_delete=models.CASCADE,
        related_name="admission"
    )

    admission_date = models.DateField(auto_now_add=True)

    student_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    batch = models.ForeignKey(
        "Batch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=50,
        default="Admitted"
    )

    def __str__(self):
        return self.student_name

