from django.db import models
from tims.users.models import User


from django.conf import settings
# Create your models here.

class Enquiry(models.Model):

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    course_id = models.ForeignKey(
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
        "adminapp.Course",
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


#class FacultyAssignment(models.Model):
   # faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    #course = models.ForeignKey(Course, on_delete=models.CASCADE)
  #  batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    #def __str__(self):
        #return f"{self.faculty} - {self.course} - {self.batch}"
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
User = get_user_model()
from django.utils.timezone import now
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

from calendar import monthrange
from datetime import date
from decimal import Decimal
from django.db import models
from django.conf import settings

class LeaveType(models.Model):

    LEAVE_CHOICES = [
        ("Casual", "Casual Leave"),
        ("Sick", "Sick Leave"),
        ("Paid", "Paid Leave"),
        ("Maternity", "Maternity Leave"),
    ]

    name = models.CharField(max_length=50, choices=LEAVE_CHOICES, unique=True)

    is_maternity = models.BooleanField(default=False)  
    # Maternity should not be divided by 12

    def __str__(self):
        return self.name

class LeaveAllocation(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)

    year = models.IntegerField(default=date.today().year)

    total_days = models.FloatField()  
    # HR assigns yearly total (example 12)

    def monthly_accrual(self):
        if self.leave_type.is_maternity:
            return 0
        return self.total_days / 12

    def __str__(self):
        return f"{self.user.username} - {self.leave_type.name} ({self.year})"


class LeaveApplication(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    DAY_TYPE = [
        ("FULL", "Full Day"),
        ("HALF", "Half Day"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    day_type = models.CharField(max_length=10, choices=DAY_TYPE, default="FULL")

    total_days = models.FloatField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    applied_at = models.DateTimeField(auto_now_add=True)

    lop_days = models.FloatField(default=0)

    reason = models.TextField(blank=True, null=True)

    def clean(self):

        today = timezone.now().date()

        # ❌ End date validation
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

        # ❌ Duplicate leave
        if LeaveApplication.objects.filter(
                user=self.user,
                start_date=self.start_date,
                status__in=["Pending", "Approved"]
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Leave already applied for this date.")

        # ❌ Past date restriction except sick
        if self.leave_type.name != "Sick":
            if self.start_date < today:
                raise ValidationError("Cannot apply leave for past date.")

        # ❌ Maternity Rule
        if self.leave_type.is_maternity:
            if hasattr(self.user, "profile"):
                if self.user.profile.gender != "Female":
                    raise ValidationError("Maternity leave allowed only for female employees.")

    def calculate_days(self):
        days = (self.end_date - self.start_date).days + 1

        if self.day_type == "HALF":
            days = 0.5

        return days

    def save(self, *args, **kwargs):
        self.clean()
        self.total_days = self.calculate_days()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type.name}"

class LeaveBalance(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    year = models.IntegerField(default=date.today().year)

    earned_days = models.FloatField(default=0)
    used_days = models.FloatField(default=0)
    lop_days = models.FloatField(default=0)

    def remaining_days(self):
        return self.earned_days - self.used_days

    def __str__(self):
        return f"{self.user.username} - {self.leave_type.name} Balance"

class Holiday(models.Model):
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=200)

    def clean(self):
        if self.date < now().date():
            raise ValidationError("Cannot add past holidays.")

    def __str__(self):
        return f"{self.date} - {self.reason}"

from django.db import models
from django.conf import settings
from decimal import Decimal
from calendar import monthrange
from datetime import date


class Salary(models.Model):

    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    MONTH_CHOICES = [
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
]

    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()

    # ===== EARNINGS =====
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    travel_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    incentive = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ===== DEDUCTIONS =====
    pf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    esi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lop_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ===== FINAL =====
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    working_days = models.IntegerField(default=0)
    lop_days = models.FloatField(default=0)

    status = models.CharField(
        max_length=10,
        choices=[("Pending", "Pending"), ("Paid", "Paid")],
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["faculty", "month", "year"],
                name="unique_salary_per_month"
            )
        ]

    def __str__(self):
        return f"{self.faculty.username} - {self.month}/{self.year}"

    # ======================================================
    #                SALARY CALCULATION LOGIC
    # ======================================================

    def calculate_salary(self):
        from .models import LeaveApplication, Holiday

        # 1️⃣ Calculate Working Days
        total_days = monthrange(self.year, self.month)[1]

        sundays = 0
        for day in range(1, total_days + 1):
            if date(self.year, self.month, day).weekday() == 6:
                sundays += 1

        holidays = Holiday.objects.filter(
            date__year=self.year,
            date__month=self.month
        ).count()

        self.working_days = total_days - sundays - holidays

        # 2️⃣ HRA = 40% of Basic
        self.hra = self.basic_salary * Decimal("0.40")

        # 3️⃣ Gross Salary
        self.gross_salary = (
            self.basic_salary
            + self.hra
            + self.travel_allowance
            + self.special_allowance
            + self.bonus
            + self.incentive
        )

        # 4️⃣ PF = 12% of Basic
        self.pf = self.basic_salary * Decimal("0.12")

        # 5️⃣ ESI = 0.75% if Gross <= 21000
        if self.gross_salary <= Decimal("21000"):
            self.esi = self.gross_salary * Decimal("0.0075")
        else:
            self.esi = Decimal("0.00")

        # 6️⃣ LOP Calculation from Approved Leaves
        leaves = LeaveApplication.objects.filter(
            user=self.faculty,
            status="Approved",
            start_date__year=self.year,
            start_date__month=self.month
        )

        self.lop_days = sum(leave.lop_days for leave in leaves)

        if self.working_days > 0:
            per_day_salary = self.gross_salary / Decimal(self.working_days)
            self.lop_deduction = per_day_salary * Decimal(self.lop_days)
        else:
            self.lop_deduction = Decimal("0.00")

        # 7️⃣ Total Deductions
        self.total_deductions = (
            self.pf
            + self.esi
            + self.lop_deduction
        )

        # 8️⃣ Net Salary
        self.net_salary = self.gross_salary - self.total_deductions

    # ======================================================
    #                     SAVE OVERRIDE
    # ======================================================

    def save(self, *args, **kwargs):
        self.calculate_salary()
        super().save(*args, **kwargs)
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
    batch_name = models.CharField(max_length=100) 
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.batch_name



class FacultyAssignment(models.Model):
    faculty = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey("adminapp.Course", on_delete=models.CASCADE)
    batch = models.ForeignKey("adminapp.Batch", on_delete=models.CASCADE)

    class Meta:
        # Enforce that each faculty can only have one assignment per course & batch
        constraints = [
            models.UniqueConstraint(
                fields=["faculty", "course", "batch"],
                name="unique_faculty_course_batch_per_faculty" 
            )
        ]

    def __str__(self):
        return f"{self.faculty} - {self.course} - {self.batch}"

    def clean(self):
        """
        Prevent duplicates for the same faculty.
        Different faculties can have same course & batch.
        """
        if FacultyAssignment.objects.filter(
            faculty=self.faculty,
            course=self.course,
            batch=self.batch
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"{self.faculty} is already assigned to this course and batch."
            )

    def save(self, *args, **kwargs):
        self.clean()  # enforce validation
        super().save(*args, **kwargs)

from django.utils import timezone

class Assignstudent(models.Model):    
    student = models.ForeignKey("users.User", on_delete=models.CASCADE)  
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    joined_on = models.DateField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    completed_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.course} ({self.batch})"

import uuid
class Certificate(models.Model):
    student = models.ForeignKey(
        Assignstudent,
        on_delete=models.CASCADE,
        related_name="certificates"
    )
    issued_on = models.DateField(auto_now_add=True)

    class Meta:
        # Prevent duplicate certificate for same student-course
        unique_together = ('student',)

    def save(self, *args, **kwargs):
        # Auto generate certificate number
        if not self.certificate_number:
            self.certificate_number = "CERT-" + str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.student} - {self.student.course}"


def yearly_leave_reset():

    current_year = date.today().year
    previous_year = current_year - 1

    balances = LeaveBalance.objects.filter(year=previous_year)

    for balance in balances:

        allocation = LeaveAllocation.objects.filter(
            user=balance.user,
            leave_type=balance.leave_type,
            year=previous_year
        ).first()

        if not allocation:
            continue

        # Carry forward ONLY Paid Leave
        if balance.leave_type.name == "Paid":

            remaining = balance.remaining_days()

            LeaveBalance.objects.update_or_create(
                user=balance.user,
                leave_type=balance.leave_type,
                year=current_year,
                defaults={
                    "earned_days": remaining,
                    "used_days": 0,
                    "lop_days": 0
                }
            )

        else:
            # Casual & Sick Reset
            LeaveBalance.objects.update_or_create(
                user=balance.user,
                leave_type=balance.leave_type,
                year=current_year,
                defaults={
                    "earned_days": 0,
                    "used_days": 0,
                    "lop_days": 0
                }
            )

def monthly_accrual():

    current_year = date.today().year

    allocations = LeaveAllocation.objects.filter(year=current_year)

    for allocation in allocations:

        if allocation.leave_type.is_maternity:
            continue

        balance, created = LeaveBalance.objects.get_or_create(
            user=allocation.user,
            leave_type=allocation.leave_type,
            year=current_year
        )

        balance.earned_days += allocation.monthly_accrual()
        balance.save()
    certificate_number = models.CharField(
        max_length=100,
        unique=True,
        blank=True
    )

    