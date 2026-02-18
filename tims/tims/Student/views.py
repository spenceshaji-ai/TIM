

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from Student.models import JobApplication,Student
from .forms import JobApplicationForm,StudentForm


from django.shortcuts import render, redirect
from django.views import View
from Student.models import Student
from .forms import StudentForm
from django.contrib.auth import get_user_model
User = get_user_model()
from adminapp.models import Batch,FacultyAssignment,Assignstudent,Batch
from tims.faculty.models import TrainingSession,FacultyDailyReport,StudentAttendance
from django.contrib.auth.mixins import LoginRequiredMixin
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


class StudentProgressView(LoginRequiredMixin, View):
    template_name = "progress.html"

    def get(self, request):

        student = request.user   # 🔐 only logged student

        # Get assigned batch
        assignment = Assignstudent.objects.filter(
            student=student
        ).select_related('batch', 'batch__course').first()

        batch = assignment.batch if assignment else None

        # Attendance calculation
        total_classes = StudentAttendance.objects.filter(
            student=student
        ).count()

        present_classes = StudentAttendance.objects.filter(
            student=student,
            status="Present"
        ).count()

        attendance_percentage = 0
        if total_classes > 0:
            attendance_percentage = round(
                (present_classes / total_classes) * 100, 2
            )

        context = {
            "student": student,
            "batch": batch,
            "course": batch.course if batch else None,
            "attendance_percentage": attendance_percentage,
            "total_classes": total_classes,
            "present_classes": present_classes,
        }

        return render(request, self.template_name, context)

class HomeView1(View):
    def get(self, request):
        return render(request, "studenthome.html")         
