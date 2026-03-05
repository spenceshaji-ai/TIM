from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from tims.adminapp.models import LeaveApplication, LeaveBalance, Salary
from django import forms




class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = [
            "leave_type",
            "start_date",
            "end_date",
            "day_type",
            "reason",
        ]

        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "day_type": forms.Select(attrs={"class": "form-control"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and end < start:
            raise forms.ValidationError("End date cannot be before start date.")

        return cleaned_data

from tims.faculty.models import TrainingSession, StudentAttendance,FacultyDailyReport
from tims.adminapp.models import Batch,FacultyAssignment,Assignstudent
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone 
from django.utils.timezone import now
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
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'max': timezone.now().date()   # 👈 prevents future in picker
                }
            ),
            'topic_covered': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter topics covered'
            }),
            'hours_taken': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['batch'].empty_label = "Select Batch"

    # 🔹 Prevent future date
    def clean_session_date(self):
        session_date = self.cleaned_data.get("session_date")

        if session_date and session_date > timezone.now().date():
            raise forms.ValidationError(
                "Future dates are not allowed."
            )

        return session_date

    # 🔹 Prevent duplicate session
    def clean(self):
        cleaned_data = super().clean()
        batch = cleaned_data.get("batch")
        session_date = cleaned_data.get("session_date")

        if batch and session_date:
            qs = TrainingSession.objects.filter(
                batch=batch,
                session_date=session_date
            )

            # If update view exists, exclude current object
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "A session for this batch already exists on this date."
                )

        return cleaned_data
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
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'max': timezone.now().date()   # UI restriction
                }
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            assigned_batches = FacultyAssignment.objects.filter(
                faculty=user
            ).values_list('batch', flat=True)

            # Show only faculty batches
            self.fields['batch'].queryset = Batch.objects.filter(
                id__in=assigned_batches
            )

            # Show students only from faculty batches
            self.fields['student'].queryset = User.objects.filter(
                assignstudent__batch__in=assigned_batches,
                role__role_name__iexact='Student'
            ).distinct()

        self.fields['batch'].empty_label = "Select Batch"
        self.fields['student'].empty_label = "Select Student"

    # 🔒 Prevent future date (Backend validation)
    def clean_attendance_date(self):
        attendance_date = self.cleaned_data.get("attendance_date")

        if attendance_date and attendance_date > timezone.now().date():
            raise forms.ValidationError("Future dates are not allowed.")

        return attendance_date

    # 🔒 Prevent duplicate attendance
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        attendance_date = cleaned_data.get('attendance_date')

        if student and attendance_date:
            qs = StudentAttendance.objects.filter(
                student=student,
                attendance_date=attendance_date
            )

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
            'report_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'max': timezone.now().date()  # Prevent future selection in UI
                }
            ),
            'start_time': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'end_time': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'activities': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'remarks': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
       
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        report_date = cleaned_data.get('report_date')

        # 1️⃣ Prevent future date
        if report_date and report_date > timezone.now().date():
            raise forms.ValidationError("Future date is not allowed.")

        # 2️⃣ Time validation
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError(
                    "End time must be greater than start time."
                )

        # 3️⃣ Duplicate validation (same faculty + date + start time)
        faculty_id = self.instance.faculty_id

        if report_date and start_time and faculty_id:
            qs = FacultyDailyReport.objects.filter(
                faculty_id=faculty_id,
                report_date=report_date,
                start_time=start_time
            )

            # Allow update case
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Report for this date and start time already exists."
                )

        return cleaned_data


