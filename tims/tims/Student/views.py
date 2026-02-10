from django.shortcuts import render, redirect
from django.views import View
from Student.models import Student
from .forms import StudentForm

class StudentRegisterView(View):
    template_name="student_register.html"

    def get(self, request):
        form = StudentForm()
        return render(
            request,
            self.template_name,
            {"form": form}
        )

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            # ✅ redirect back to registration page
            return redirect("Student:student_register")

        # ❌ if form is invalid, show same page with errors
        return render(
            request,
            self.template_name,
            {"form": form}
        )
