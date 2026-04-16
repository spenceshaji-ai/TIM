from django import forms
from django.core.exceptions import ValidationError
from datetime import date,datetime
from tims.adminapp.models import LeaveApplication, LeaveBalance, Salary
from django import forms




class LeaveApplicationForm(forms.ModelForm):

    HALF_SESSION_CHOICES = [
        ("Morning", "Morning"),
        ("Noon", "Noon"),
    ]

    # ✅ IMPORTANT FIX (same as admin)
    half_day_session = forms.ChoiceField(
        choices=[("", "Select")] + HALF_SESSION_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            balances = LeaveBalance.objects.filter(
                user=self.user,
                year=date.today().year
            ).values_list("leave_type", flat=True)

            self.fields["leave_type"].queryset = self.fields["leave_type"].queryset.filter(
                id__in=balances
            )

    def clean(self):

        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        day_type = cleaned_data.get("day_type")
        half_session = cleaned_data.get("half_day_session")

        today = date.today()
        current_time = now().time()

        # ✅ BASIC VALIDATIONS
        if start and start < today:
            raise ValidationError("Past dates are not allowed.")

        if start and end and end < start:
            raise ValidationError("End date cannot be before start date.")

        if start and self.user:
            exists = LeaveApplication.objects.filter(
                user=self.user,
                start_date=start,
                status__in=["Pending", "Approved"]
            ).exists()

            if exists:
                raise ValidationError("You already applied leave for this date.")

        # ✅ HALF DAY LOGIC
        if day_type == "HALF":

            if not half_session:
                raise ValidationError("Select Morning or Noon for half day.")

            if start == today:

                if current_time >= datetime.strptime("09:30", "%H:%M").time():
                    if half_session == "Morning":
                        raise ValidationError(
                            "Morning half day cannot be applied after 9:30 AM."
                        )

                if current_time >= datetime.strptime("12:30", "%H:%M").time():
                    raise ValidationError(
                        "Half day leave cannot be applied after 12:30 PM."
                    )

        # ✅ NEW JOINER RULE (NO BLOCKING — SAME AS ADMIN)
        if self.user and start:

            joining_date = self.user.date_joined.date()

            if (today - joining_date).days < 365:

                month_leaves = LeaveApplication.objects.filter(
                    user=self.user,
                    start_date__year=start.year,
                    start_date__month=start.month,
                    status__in=["Pending", "Approved"]
                )

                total_taken = 0

                for leave in month_leaves:
                    if leave.day_type == "HALF":
                        total_taken += 0.5
                    else:
                        total_taken += (
                            (leave.end_date - leave.start_date).days + 1
                        )

                current_days = 0.5 if day_type == "HALF" else (
                    (end - start).days + 1
                )

                # ❗ DO NOT raise error (LOP handled in view)
                pass

        return cleaned_data

from tims.faculty.models import TrainingSession, StudentAttendance,FacultyDailyReport,BatchCompletionRequest
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


from tims.faculty.models import FacultyCourseMaterial
from tims.adminapp.models import FacultyAssignment, Course, Batch

class FacultyCourseMaterialForm(forms.ModelForm):
    class Meta:
        model = FacultyCourseMaterial
        fields = [
            "course",
            "batch",
            "title",
            "description",
            "material_type",
            "pdf_file",
            "image_file",
            "video_url",
        ]
        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "batch": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "material_type": forms.Select(attrs={"class": "form-control"}),
            "pdf_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "image_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "video_url": forms.URLInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.faculty = kwargs.pop("faculty", None)
        super().__init__(*args, **kwargs)

        if self.faculty:
            # Get all courses and batches assigned to this faculty
            assignments = FacultyAssignment.objects.filter(faculty=self.faculty)
            assigned_courses = assignments.values_list('course', flat=True).distinct()
            assigned_batches = assignments.values_list('batch', flat=True).distinct()

            # Set queryset for dropdowns
            self.fields['course'].queryset = Course.objects.filter(id__in=assigned_courses)
            self.fields['batch'].queryset = Batch.objects.filter(id__in=assigned_batches)


class BatchCompletionRequestForm(forms.ModelForm):
    class Meta:
        model = BatchCompletionRequest
        fields = ["batch", "requested_completion_date", "remarks"]
        widgets = {
            "batch": forms.Select(attrs={"class": "form-select"}),
            "requested_completion_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "remarks": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control"
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

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

        if not batch or not request_date or not self.user:
            return cleaned_data

        # 1) Batch must belong to faculty
        is_assigned = FacultyAssignment.objects.filter(
            faculty=self.user,
            batch=batch
        ).exists()

        if not is_assigned:
            self.add_error("batch", "You are not assigned to this batch.")
            return cleaned_data

        # 2) Training sessions must exist
        has_sessions = TrainingSession.objects.filter(
            faculty=self.user,
            batch=batch
        ).exists()

        if not has_sessions:
            self.add_error(
                "batch",
                "No training sessions have been added for this batch, so completion request cannot be submitted."
            )

        # 3) Batch end date must be reached
        today = timezone.localdate()
        if batch.end_date and batch.end_date > today:
            self.add_error(
                "batch",
                f"Completion request can only be submitted on or after the batch end date ({batch.end_date})."
            )

        # 4) Requested completion date must be on or after batch end date
        if batch.end_date and request_date < batch.end_date:
            self.add_error(
                "requested_completion_date",
                f"Completion date must be on or after batch end date ({batch.end_date})."
            )

        # 5) Prevent duplicate pending request
        pending_exists = BatchCompletionRequest.objects.filter(
            faculty=self.user,
            batch=batch,
            course=batch.course,
            status="Pending"
        ).exists()

        if pending_exists:
            self.add_error(
                "batch",
                "A pending completion request already exists for this batch."
            )

        # 6) Prevent duplicate approved request
        approved_exists = BatchCompletionRequest.objects.filter(
            faculty=self.user,
            batch=batch,
            course=batch.course,
            status="Approved"
        ).exists()

        if approved_exists:
            self.add_error(
                "batch",
                "This batch has already been approved as completed."
            )

        return cleaned_data