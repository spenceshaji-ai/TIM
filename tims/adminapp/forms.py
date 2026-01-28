from django import forms
from .models import Course,Batch

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
            "faculty",
        ]

        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "faculty": forms.Select(attrs={"class": "form-control"}),
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
