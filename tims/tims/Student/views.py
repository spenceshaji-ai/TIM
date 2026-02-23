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
            return redirect("Student:student_register")

        # ❌ if form is invalid, show same page with errors
        return render(
            request,
            self.template_name,
            {"form": form}
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

class StudentTrainingSessionView(LoginRequiredMixin, View):
    template_name = "training_sessions.html"

    def get(self, request):

        # Assigned batch & course for this student
        student_assignments = Assignstudent.objects.filter(
            student=request.user
        ).select_related("batch", "course")

        batch_ids = student_assignments.values_list("batch_id", flat=True)

        # Only approved sessions
        sessions = TrainingSession.objects.filter(
            batch_id__in=batch_ids,
            approval_status="Approved"
        ).select_related("batch", "faculty").order_by("-session_date")

        context = {
            "sessions": sessions,
            "student_assignments": student_assignments
        }

        return render(request, self.template_name, context)


class HomeView1(View):
    def get(self, request):
        return render(request, "studenthome.html")         