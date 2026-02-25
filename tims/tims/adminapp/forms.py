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
from adminapp.models import Salary, Holiday

from django import forms


from django.utils.timezone import now


class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        fields = [
            "faculty",
            "month",
            "year",
            "basic_salary",
            "travel_allowance",
            "special_allowance",
            "bonus",
            "incentive",
        ]

        widgets = {
            "faculty": forms.Select(attrs={"class": "form-control"}),
            "month": forms.Select(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": "readonly"
            }),
            "basic_salary": forms.NumberInput(attrs={"class": "form-control"}),
            "travel_allowance": forms.NumberInput(attrs={"class": "form-control"}),
            "special_allowance": forms.NumberInput(attrs={"class": "form-control"}),
            "bonus": forms.NumberInput(attrs={"class": "form-control"}),
            "incentive": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Auto Year
        if not self.instance.pk:
            self.fields["year"].initial = now().year

        # Hide faculty field if coming from user-wise page
        if self.initial.get("faculty"):
            self.fields["faculty"].widget = forms.HiddenInput()

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