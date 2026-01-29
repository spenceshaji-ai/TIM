from django import forms
from Student.models import Student,JobApplication

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'phone',
            # 'course',
            'passout_year',
            'qualification',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter full name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter phone number',
                'class': 'form-control'
            }),

            # # ✅ ForeignKey → Dropdown
            # 'course': forms.Select(attrs={
            #     'class': 'form-control'
            # }),

            'passout_year': forms.NumberInput(attrs={
                'placeholder': 'Enter passout year',
                'class': 'form-control'
            }),
            'qualification': forms.TextInput(attrs={
                'placeholder': 'Enter qualification',
                'class': 'form-control'
            }),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job', 'resume', 'applied_date']

        widgets = {
            'job': forms.Select(attrs={'class': 'form-control'}),
            'applied_date': forms.DateInput(attrs={'type': 'date'}),
        }
