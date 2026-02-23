from django import forms
from .models import FacultyCourseMaterial
from adminapp.models import FacultyAssignment, Course, Batch

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
