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

    half_day_session = forms.ChoiceField(
        choices=HALF_SESSION_CHOICES,
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

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        day_type = cleaned_data.get("day_type")
        half_session = cleaned_data.get("half_day_session")

        today = date.today()
        current_time = now().time()

        # ❌ No past dates
        if start and start < today:
            raise ValidationError("Past dates are not allowed.")

        # ❌ End date validation
        if start and end and end < start:
            raise ValidationError("End date cannot be before start date.")

        # ❌ Prevent duplicate leave request same day
        if start and self.user:
            exists = LeaveApplication.objects.filter(
                user=self.user,
                start_date=start,
                status__in=["Pending", "Approved"]
            ).exists()

            if exists:
                raise ValidationError("You already applied leave for this date.")

        # HALF DAY LOGIC
        if day_type == "Half":

            if not half_session:
                raise ValidationError("Select Morning or Noon for half day.")

            # Today's leave restrictions
            if start == today:

                # After 9:30 → Morning not allowed
                if current_time >= datetime.strptime("09:30", "%H:%M").time():
                    if half_session == "Morning":
                        raise ValidationError(
                            "Morning half day cannot be applied after 9:30 AM."
                        )

                # After 12:30 → No half day allowed
                if current_time >= datetime.strptime("12:30", "%H:%M").time():
                    raise ValidationError(
                        "Half day leave cannot be applied after 12:30 PM."
                    )

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
