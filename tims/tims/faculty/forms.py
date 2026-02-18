from django import forms
from .models import TrainingSession, StudentAttendance,FacultyDailyReport
from adminapp.models import Batch,FacultyAssignment,Assignstudent
from django.contrib.auth import get_user_model
User = get_user_model()


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = [
            'batch',
            'session_date',
            'topic_covered',
            'hours_taken',
            'status',
        ]

        widgets = {
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'session_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'topic_covered': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Enter topics covered in this session'
                }
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
        self.fields['batch'].empty_label = "Select Batch"

class StudentAttendanceForm(forms.ModelForm):

    class Meta:
        model = StudentAttendance
        fields = [
            'batch',
            'student',
            'attendance_date',
            'status',
        ]

        widgets = {
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'attendance_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Get batches assigned to faculty
            assigned_batches = FacultyAssignment.objects.filter(
                faculty=user
            ).values_list('batch', flat=True)

            # Show only those batches
            self.fields['batch'].queryset = Batch.objects.filter(
                id__in=assigned_batches
            )

            # Show only students assigned to those batches
            self.fields['student'].queryset = User.objects.filter(
                assignstudent__batch__in=assigned_batches,
                role__role_name__iexact='Student'
            )

        self.fields['batch'].empty_label = "Select Batch"
        self.fields['student'].empty_label = "Select Student"

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        attendance_date = cleaned_data.get('attendance_date')

        if student and attendance_date:
            qs = StudentAttendance.objects.filter(
                student=student,
                attendance_date=attendance_date
            )

            # Allow updating same record
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Attendance for this student on this date already exists."
                )

        return cleaned_data
class FacultyDailyReportForm(forms.ModelForm):

    class Meta:
        model = FacultyDailyReport
        fields = [
            'report_date',
            'start_time',
            'end_time',
            'activities',
            'remarks',
        ]

        widgets = {
            'report_date': forms.DateInput(attrs={'class': 'form-control','type': 'date' }),
            'start_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
            'activities': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            'remarks': forms.Textarea(attrs={'class': 'form-control','rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        report_date = cleaned_data.get('report_date')

        # 1️⃣ Time validation
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError(
                    "End time must be greater than start time."
                )

        # 2️⃣ Duplicate validation
        faculty_id = self.instance.faculty_id

        if report_date and start_time and faculty_id:

            qs = FacultyDailyReport.objects.filter(
                faculty_id=faculty_id,
                report_date=report_date,
                start_time=start_time
            )

            # Allow update (exclude current record)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Report for this date and start time already exists."
                )

        return cleaned_data


