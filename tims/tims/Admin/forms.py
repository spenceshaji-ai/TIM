from django import forms
from Admin.models import Job,Jobtype,Interview
from Student.models import JobApplication


class JobtypeForm(forms.ModelForm):
    class Meta:
        model = Jobtype
        fields = ['job_type']
        widgets = {
            'job_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job type'}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'job_type', 'salary']

        labels = {
            'job_type': 'Job Type',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job location',
            }),
            'job_type': forms.Select(attrs={
                'class': 'form-control',
            }),  # <-- FIXED: use Select for ForeignKey
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary',
            }),
        }




class ScheduleInterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'feedback']
        widgets = {
            'interview_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }