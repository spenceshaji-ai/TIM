from django import forms
from .models import TrainingSession, StudentAttendance,FacultyDailyReport,BatchCompletionRequest
from adminapp.models import Batch,FacultyAssignment,Assignstudent
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
        ]
        widgets = {
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'session_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'max': timezone.now().date()
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['batch'].empty_label = "Select Batch"

    # Prevent future date
    def clean_session_date(self):
        session_date = self.cleaned_data.get("session_date")

        if session_date and session_date > timezone.now().date():
            raise forms.ValidationError("Future dates are not allowed.")

        return session_date

    # Prevent duplicate session
    def clean(self):
        cleaned_data = super().clean()
        batch = cleaned_data.get("batch")
        session_date = cleaned_data.get("session_date")

        if batch and session_date:
            qs = TrainingSession.objects.filter(
                batch=batch,
                session_date=session_date
            )

            # Exclude current object during update
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "A session for this batch already exists on this date."
                )

        return cleaned_data

class AttendanceFilterForm(forms.Form):
    batch = forms.ModelChoiceField(
        queryset=Batch.objects.none(),
        required=True,
        empty_label="Select Batch"
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # ✅ Show only batches assigned to faculty
            self.fields['batch'].queryset = Batch.objects.filter(
                facultyassignment__faculty=user
            )

        # ✅ Disable future dates in UI
        today = timezone.now().date()
        self.fields['date'].widget.attrs['max'] = today

    # ✅ Backend validation (important)
    def clean_date(self):
        date = self.cleaned_data['date']
        today = timezone.now().date()

        if date > today:
            raise forms.ValidationError("Future date is not allowed.")

        return date

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

class BatchCompletionRequestForm(forms.ModelForm):
    class Meta:
        model = BatchCompletionRequest
        fields = ["batch", "requested_completion_date", "remarks"]
        widgets = {
            "batch": forms.Select(attrs={"class": "form-select"}),
            "requested_completion_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "remarks": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        # Show only assigned batches of logged-in faculty
        assigned_batch_ids = FacultyAssignment.objects.filter(
            faculty=user
        ).values_list("batch_id", flat=True)

        self.fields["batch"].queryset = Batch.objects.filter(
            id__in=assigned_batch_ids
        ).select_related("course")

        self.fields["batch"].empty_label = "Select Batch"

    def clean_requested_completion_date(self):
        request_date = self.cleaned_data.get("requested_completion_date")
        today = timezone.localdate()

        if request_date and request_date > today:
            raise forms.ValidationError("Future completion date is not allowed.")

        return request_date

    def clean(self):
        cleaned_data = super().clean()
        batch = cleaned_data.get("batch")
        request_date = cleaned_data.get("requested_completion_date")

        if not batch or not self.user:
            return cleaned_data

        # Auto-fill course from batch
        cleaned_data["course"] = batch.course

        return cleaned_data

