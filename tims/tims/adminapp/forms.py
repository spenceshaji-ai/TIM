from django import forms
from adminapp.models import LeaveApplication, LeaveBalance, Salary
from django.core.exceptions import ValidationError

from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from adminapp.models import LeaveApplication

from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from adminapp.models import LeaveApplication, LeaveBalance, Salary


from django.contrib.auth import get_user_model

from adminapp.models import Course, Batch, FacultyAssignment,Assignstudent

User = get_user_model()


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["course_name", "duration", "syllabus", "fee"]

        widgets = {
            "course_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter course name"
            }),
            "duration": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 3 Months"
            }),
            "syllabus": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter syllabus details"
            }),
            "fee": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter course fee"
            }),
        }

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            "course",
            "batch_name",
            "start_date",
            "end_date",
            "capacity",
            
        ]
        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "batch_name": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "end_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
        }

class FacultyAssignmentForm(forms.ModelForm):
    class Meta:
        model = FacultyAssignment
        fields = [
            "faculty",
            "course",
            "batch",
        ]
        widgets = {
            "faculty": forms.Select(attrs={"class": "form-control"}),
            "course": forms.Select(attrs={"class": "form-control"}),
            "batch": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)

     self.fields["faculty"].queryset = User.objects.filter(role__isnull=False)


class AssignstudentForm(forms.ModelForm):
    class Meta:
        model = Assignstudent
        fields = ["student", "course", "batch"]
        widgets = {
            "student": forms.Select(attrs={"class": "form-control"}),
            "course": forms.Select(attrs={"class": "form-control"}),
            "batch": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = User.objects.filter(
            role__role_name="student"
        )






class LeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        fields = [
            "user",
            "leave_type",
            "year",
            "earned_days",
        ]

        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "leave_type": forms.Select(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "earned_days": forms.NumberInput(attrs={"class": "form-control"}),
        }

from django import forms
from adminapp.models import LeaveAllocation, LeaveType


from django import forms
from adminapp.models import LeaveAllocation, LeaveType


class HRLeaveAllocationForm(forms.ModelForm):

    class Meta:
        model = LeaveAllocation
        fields = ["leave_type", "total_days"]

        widgets = {
            "leave_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "total_days": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "step": "0.5"
            }),
        }

        labels = {
            "leave_type": "Leave Type",
            "total_days": "Total Days",
        }

    def __init__(self, *args, **kwargs):

        # These come from the view
        self.user = kwargs.pop("employee", None)
        self.year = kwargs.pop("year", None)

        super().__init__(*args, **kwargs)

        # Show all leave types
        self.fields["leave_type"].queryset = LeaveType.objects.all()

    def clean(self):

        cleaned_data = super().clean()
        leave_type = cleaned_data.get("leave_type")

        if self.user and leave_type and self.year:

            # Prevent duplicate allocation for same year
            existing = LeaveAllocation.objects.filter(
                user=self.user,
                leave_type=leave_type,
                year=self.year
            )

            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise forms.ValidationError(
                    "Leave already allocated for this type in this year."
                )

        return cleaned_data
    
from django import forms
from adminapp.models import Salary, Holiday

from django import forms


from django.utils.timezone import now




class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ["date", "reason"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": date.today().isoformat(),
                    "class": "form-control"
                }
            ),
            "reason": forms.TextInput(
                attrs={"class": "form-control"}
            )
        }

from django import forms
from django.utils.timezone import now
from adminapp.models import Salary, SalaryStructure


# ============================================
# 1️⃣ Salary Structure Form (One Time Setup)
# ============================================

# forms.py

class SalaryStructureForm(forms.ModelForm):

    class Meta:
        model = SalaryStructure
        fields = [
            "basic_salary",
            "travel_allowance",
            "special_allowance",
        ]

        widgets = {
            "basic_salary": forms.NumberInput(attrs={"class": "form-control"}),
            "travel_allowance": forms.NumberInput(attrs={"class": "form-control"}),
            "special_allowance": forms.NumberInput(attrs={"class": "form-control"}),
        }

# ============================================
# 2️⃣ Monthly Salary Form
# ============================================
# forms.py




class MonthlySalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ["faculty", "year", "month", "bonus", "incentive"]

        widgets = {
            "faculty": forms.HiddenInput(),
            "year": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": "readonly"
            }),
            "month": forms.Select(attrs={"class": "form-control"}),
            "bonus": forms.NumberInput(attrs={"class": "form-control"}),
            "incentive": forms.NumberInput(attrs={"class": "form-control"}),
        }