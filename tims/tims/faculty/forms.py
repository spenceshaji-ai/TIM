from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from adminapp.models import LeaveApplication, LeaveBalance, Salary
from django import forms




class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = [
            "leave_type",
            "start_date",
            "end_date",
            "day_type",
            "reason",
        ]

        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "day_type": forms.Select(attrs={"class": "form-control"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and end < start:
            raise forms.ValidationError("End date cannot be before start date.")

        return cleaned_data