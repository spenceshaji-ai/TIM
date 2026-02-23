from django import forms
from .models import Student, Feedback  # ✅ same-app relative import

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
        }
