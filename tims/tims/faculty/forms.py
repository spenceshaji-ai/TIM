from django import forms
from .models import TrainingSession, StudentAttendance
from adminapp.models import Batch
from django.contrib.auth import get_user_model
User = get_user_model()


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = [
            'batch',
            'faculty',
            'session_date',
            'topic_covered',
            'hours_taken',
            'status',
        ]

        widgets = {
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'session_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'} ),
            'topic_covered': forms.Textarea(attrs={ 'class': 'form-control', 'rows': 3,
                    'placeholder': 'Enter topics covered in this session' }
            ),
            'hours_taken': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.5',
                    'min': '0',
                    'placeholder': 'e.g. 2.5'
                }
            ),

            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show ONLY Faculty role users
        self.fields['faculty'].queryset = User.objects.filter(
            role__role_name__iexact='Faculty'
        )

        self.fields['batch'].empty_label = "Select Batch"
        self.fields['faculty'].empty_label = "Select Faculty"

class StudentAttendanceForm(forms.ModelForm):

    class Meta:
        model = StudentAttendance
        fields = [
            'student',
            'faculty',
            'batch',
            'attendance_date',
            'status',
        ]

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'attendance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only students
        self.fields['student'].queryset = User.objects.filter(
            role__role_name__iexact='Student'
        ).order_by('username')

        # Only faculty
        self.fields['faculty'].queryset = User.objects.filter(
            role__role_name__iexact='Faculty'
        ).order_by('username')

        self.fields['student'].empty_label = "Select Student"
        self.fields['faculty'].empty_label = "Select Faculty"
        self.fields['batch'].empty_label = "Select Batch"

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        attendance_date = cleaned_data.get('attendance_date')

        if student and attendance_date:
            qs = StudentAttendance.objects.filter(
                student=student,
                attendance_date=attendance_date
         )

        # Allow updating the same record
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Attendance for this student on this date already exists."
                )

        return cleaned_data



