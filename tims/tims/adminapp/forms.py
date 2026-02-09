from django import forms

from adminapp.models import Enquiry
from adminapp.models import FollowUp
from adminapp.models import Admission
from adminapp.models import Course,Batch

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

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            "course",
            "batch_name",
            "start_date",
            "end_date",
            "capacity",
            "faculty",
        ]

        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "faculty": forms.Select(attrs={"class": "form-control"}),
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

class EnquiryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Populate dropdown with courses
        self.fields["course"].queryset = Course.objects.all()

        # ✅ Optional: Add placeholder
        self.fields["course"].empty_label = "Select Course"
    class Meta:
        model = Enquiry

        fields = [
            "name",
            "phone",
            "email",
            "course",
            "source",
            "status",
        ]

        widgets = {

            # Name
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Enquiry Person Name"
            }),

            # Phone
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Phone Number"
            }),

            # Email
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Email Address"
            }),

            # Course Dropdown
            "course": forms.Select(attrs={
                "class": "form-control"
            }),

            # Source Dropdown
            "source": forms.Select(attrs={
                "class": "form-control"
            }),

            # Status Dropdown
            "status": forms.Select(attrs={
                "class": "form-control"
            }),
        }





class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp

        fields = [
            "followup_date",
            "remarks",
            "status",
        ]

        widgets = {

            "followup_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter Follow Up Remarks",
                "rows": 3
            }),

            "status": forms.Select(attrs={
                "class": "form-control"
            }),
        }


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission

        fields = [
            "student_name",
            "phone",
            "email",
            "course",
            "batch",
            "total_fees",
            "fees_paid",
        ]

        widgets = {

            "student_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Student Full Name"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone Number"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email Address"
            }),

            "course": forms.Select(attrs={
                "class": "form-control"
            }),

            "batch": forms.Select(attrs={
                "class": "form-control"
            }),

            "total_fees": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "fees_paid": forms.NumberInput(attrs={
                "class": "form-control"
            }),
        }
#class FacultyAssignmentForm(forms.ModelForm):
   # class Meta:
      #  model = FacultyAssignment
        #fields = [
         #   "faculty",
           # "course",
           # "batch",
       # ]

      # widgets = {
           # "faculty": forms.Select(attrs={"class": "form-control"}),
           # "course": forms.Select(attrs={"class": "form-control"}),
           # "batch": forms.Select(attrs={"class": "form-control"}),
       # }

    #def __init__(self, *args, **kwargs):
       # super().__init__(*args, **kwargs)

        # Optional: only staff as faculty
       # self.fields["faculty"].queryset = User.objects.filter(is_staff=True)
