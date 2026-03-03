from django import forms
from tims.Admin.models import Job,Jobtype,Interview
from tims.Student.models import JobApplication


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
        fields = [
            'title',
            'company',
            'location',
            'job_type',
            'salary',
            'application_deadline'   
        ]

        labels = {
            'job_type': 'Job Type',
            'application_deadline': 'Application Deadline'
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
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary',
            }),
            'application_deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
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