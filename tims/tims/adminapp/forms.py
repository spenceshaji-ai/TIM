from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from tims.users.models import Role
from adminapp.models import Course, Batch, FacultyAssignment,Assignstudent,Certificate


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["course_name", "duration", "syllabus", "fee"]

        widgets = {
            "course_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter course name"
            }),
            "duration": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 3 Months"
            }),
            "syllabus": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter syllabus details"
            }),
            "fee": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter course fee"
            }),
        }

    def clean_course_name(self):
        course_name = self.cleaned_data.get("course_name")

        # Case-insensitive duplicate check
        qs = Course.objects.filter(course_name__iexact=course_name)

        # Exclude current instance when updating
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("A course with this name already exists.")

        return course_name

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            "course",
            "batch_name",
            "start_date",
            "end_date",
            "capacity",
        ]

        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "batch_name": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "end_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get("course")
        batch_name = cleaned_data.get("batch_name")

        if course and batch_name:
            qs = Batch.objects.filter(
                course=course,
                batch_name__iexact=batch_name.strip()
            )

            # Exclude current instance while updating
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "A batch with this name already exists for the selected course."
                )

        return cleaned_data

class FacultyAssignmentForm(forms.ModelForm):
    class Meta:
        model = FacultyAssignment
        fields = [
            "faculty",
            "course",
            "batch",
        ]
        widgets = {
            "faculty": forms.Select(attrs={"class": "form-control"}),
            "course": forms.Select(attrs={"class": "form-control"}),
            "batch": forms.Select(attrs={"class": "form-control"}),
        }

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    faculty_role = Role.objects.filter(role_name="Faculty").first()

    if faculty_role:
        self.fields["faculty"].queryset = User.objects.filter(
        role=faculty_role,
            status="active"
        )
    else:
        self.fields["faculty"].queryset = User.objects.none()






class AssignstudentForm(forms.ModelForm):
    class Meta:
        model = Assignstudent
        fields = [
            "student",
            "course",
            "batch",
            "joined_on",
            "is_completed",
            "completed_on",
        ]
        widgets = {
            "student": forms.Select(attrs={"class": "form-control"}),
            "course": forms.Select(attrs={"class": "form-control"}),
            "batch": forms.Select(attrs={"class": "form-control"}),
            "joined_on": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "completed_on": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        # Pop custom queryset from kwargs if provided
        students_queryset = kwargs.pop('students_queryset', None)
        super().__init__(*args, **kwargs)

        if students_queryset is not None:
            self.fields["student"].queryset = students_queryset
        else:
            # fallback to all students if no queryset provided
            self.fields["student"].queryset = User.objects.filter(
                role__role_name="student"
            )

from django import forms
from adminapp.models import Certificate, Assignstudent


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ["student"]
        widgets = {
            "student": forms.Select(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        completed_students = Assignstudent.objects.filter(
            is_completed=True
        ).exclude(certificates__isnull=False)
        self.fields["student"].queryset = completed_students

        # Use `name` instead of get_full_name
        self.fields["student"].label_from_instance = lambda obj: f"{obj.student.name} - {obj.course.course_name} ({obj.batch.batch_name})"
