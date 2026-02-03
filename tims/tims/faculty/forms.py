from django import forms
from .models import TrainingSession, StudentAttendance



class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = [
            #'batch',
            #'faculty',
            'session_date',
            'topic_covered',
            'hours_taken',
            'status',
            'approval_status',   
        ]

        widgets = {
            #'batch': forms.Select(attrs={'class': 'form-control'}),
            #'faculty': forms.Select(attrs={'class': 'form-control'}),
            'session_date': forms.DateInput(attrs={'class': 'form-control',
                'type': 'date'
            }),
            'topic_covered': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Enter topics covered',
                'rows': 4
            }),
            'hours_taken': forms.NumberInput(attrs={'class': 'form-control','step': '0.5','placeholder': 'Hours taken'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approval_status': forms.Select(attrs={'class': 'form-control'}),
        }

class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = [#'student',
         #'faculty',
         #'batch',
        'attendance_date', 'status']

        widgets = {
            #'student': forms.Select(attrs={'class': 'form-control'}),
            #'faculty': forms.Select(attrs={'class': 'form-control'}),
            #'batch': forms.Select(attrs={'class': 'form-control'}),
            'attendance_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }