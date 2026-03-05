from django import forms
from tims.Student.models import Student,JobApplication
from .models import Student, Feedback  # ✅ same-app relative import

from tims.adminapp.models import Course  
from django.contrib.auth import get_user_model
User = get_user_model()


# Student Registration
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'phone',
            'course',
            'passout_year',
            'qualification',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number', 'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'passout_year': forms.NumberInput(attrs={'placeholder': 'Enter passout year', 'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'placeholder': 'Enter qualification', 'class': 'form-control'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write your feedback..."
            }),
            'qualification': forms.TextInput(attrs={
                'placeholder': 'Enter qualification',
                'class': 'form-control'
            }),
        }

#Student Job Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["resume"]

        widgets = {
            "resume": forms.FileInput(attrs={
                "class": "form-control",
                "accept": ".pdf,.doc,.docx"
            })
        }

        labels = {
            "resume": "Upload Resume"
        }

        help_texts = {
            "resume": "Allowed formats: PDF, DOC, DOCX"
        }
