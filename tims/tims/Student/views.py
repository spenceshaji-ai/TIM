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

from django.views import View
from django.shortcuts import render, redirect


class StudentDashboardView(View):

    template_name = "student/stdhome.html"

    def get(self, request):

        # 🔐 Force password change check
        if request.user.must_change_password:
            return redirect("users:change_password")

        return render(request, self.template_name)

class stdHome(View):
    def get(self, request):

        # 🔐 force password change
        if request.user.must_change_password:
            return redirect("users:change_password")

        return render(request, "student/stdhome.html")