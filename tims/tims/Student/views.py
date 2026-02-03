

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from Student.models import JobApplication,Student
from .forms import JobApplicationForm,StudentForm


class StudentRegisterView(View):

    def get(self, request):
        form = StudentForm()
        return render(
            request,
            "admin/student_register.html",
            {"form": form}
        )

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            # ✅ redirect back to registration page
            return redirect("student_register")

        # ❌ If invalid, show errors on same page
        return render(
            request,
            "admin/student_register.html",
            {"form": form}
        )

class JobApplicationCreateView(View):
    def get(self, request):
        form = JobApplicationForm()
        return render(request, 'admin/application_create.html', {'form': form})

    def post(self, request):
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # status defaults to "Applied"
            return redirect('application_list')

        return render(request, 'admin/application_create.html', {'form': form})

class JobApplicationListView(View):
    def get(self, request):
        applications = JobApplication.objects.select_related('job', 'student')
        return render(
            request,
            'admin/application_list.html',
            {'applications': applications}
        )

class JobApplicationEditView(View):
    def get(self, request, id):
        application = get_object_or_404(JobApplication, id=id)
        form = JobApplicationForm(instance=application)
        return render(
            request,
            'admin/application_edit.html',
            {'form': form, 'application': application}
        )

    def post(self, request, id):
        application = get_object_or_404(JobApplication, id=id)
        form = JobApplicationForm(
            request.POST,
            request.FILES,
            instance=application
        )

        if form.is_valid():
            form.save()
            return redirect('application_list')

        return render(
            request,
            'admin/application_edit.html',
            {'form': form, 'application': application}
        )
