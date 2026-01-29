from django import forms
from .models import Job,JobApplication,Student

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'job_type', 'salary']

        labels = {
            'job_type': 'Job Type',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter job title',
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Company name',
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Job location',
            }),
            'job_type': forms.Select(),
            'salary': forms.NumberInput(attrs={
                'placeholder': 'Enter salary',
            }),
        }


