from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from .models import TrainingSession,StudentAttendance,FacultyDailyReport
from django.contrib.auth import get_user_model
User = get_user_model()
from adminapp.models import Batch,FacultyAssignment,Assignstudent,Batch
from .forms import TrainingSessionForm,StudentAttendanceForm,FacultyDailyReportForm


class TrainingSessionCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'create_session.html'

    # 🔐 Faculty Role Check
    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and
            user.role and
            user.role.role_name.lower() == "faculty"
        )

    # 🚫 If Not Authorized
    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to access this page.")
        return redirect("users:login")

    def get_assigned_batches(self, user):
        return Batch.objects.filter(
            id__in=FacultyAssignment.objects.filter(
                faculty=user
            ).values_list('batch', flat=True)
        )

    def get(self, request):
        form = TrainingSessionForm()
        form.fields['batch'].queryset = self.get_assigned_batches(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TrainingSessionForm(request.POST)
        form.fields['batch'].queryset = self.get_assigned_batches(request.user)

        if form.is_valid():
            try:
                session = form.save(commit=False)
                session.faculty = request.user
                session.save()
                return redirect('faculty:training_list')
            except IntegrityError:
                form.add_error(None, "Duplicate session for this batch on this date.")

        return render(request, self.template_name, {'form': form})

class TrainingSessionListView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'Session_list.html'

    # 🔐 Faculty Role Check
    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and
            user.role and
            user.role.role_name.lower() == "faculty"
        )

    # 🚫 If Not Authorized
    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to access this page.")
        return redirect("users:login")

    def get(self, request):
        sessions = TrainingSession.objects.filter(
            faculty=request.user
        ).order_by('-session_date')

        return render(request, self.template_name, {'sessions': sessions})

class TrainingSessionUpdateView(LoginRequiredMixin, View):
    template_name = 'create_session.html'

    def get(self, request, pk):
        session = get_object_or_404(
            TrainingSession,
            pk=pk,
            faculty=request.user
        )

        # 🚫 Block if Approved or Rejected
        if session.approval_status in ["Approved", "Rejected"]:
            return redirect('faculty:training_list')

        form = TrainingSessionForm(instance=session)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        session = get_object_or_404(
            TrainingSession,
            pk=pk,
            faculty=request.user
        )

        # 🚫 Block if Approved or Rejected
        if session.approval_status in ["Approved", "Rejected"]:
            return redirect('faculty:training_list')

        form = TrainingSessionForm(request.POST, instance=session)

        if form.is_valid():
            updated_session = form.save(commit=False)
            updated_session.faculty = request.user
            updated_session.save()
            return redirect('faculty:training_list')

        return render(request, self.template_name, {'form': form})
                
class TrainingSessionDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        session = get_object_or_404(
            TrainingSession,
            pk=pk,
            faculty=request.user
        )

        # 🚫 Block if Approved or Rejected
        if session.approval_status in ["Approved", "Rejected"]:
            return redirect('faculty:training_list')

        session.delete()
        return redirect('faculty:training_list')


class StudentAttendanceCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'create_attendance.html'

    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and
            user.role and
            user.role.role_name.lower() == "faculty"
        )

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to access this page.")
        return redirect("users:login")

    def get(self, request):
        form = StudentAttendanceForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StudentAttendanceForm(request.POST, user=request.user)

        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.faculty = request.user   # 🔐 secure
            attendance.save()

            messages.success(request, "Attendance created successfully.")
            return redirect('faculty:attendance-list')

        return render(request, self.template_name, {'form': form})

class StudentAttendanceListView(LoginRequiredMixin, View):
    template_name = "attendance_list.html"

    def get(self, request):
        attendances = StudentAttendance.objects.filter(
            faculty=request.user   # 🔐 only logged-in faculty
        ).select_related('student', 'batch').order_by('-attendance_date')

        return render(request, self.template_name, {
            'attendances': attendances
        })

class StudentAttendanceUpdateView(LoginRequiredMixin, View):
    template_name = "create_attendance.html"

    def get(self, request, pk):
        attendance = get_object_or_404(
            StudentAttendance,
            pk=pk,
            faculty=request.user   # 🔐 restrict ownership
        )

        form = StudentAttendanceForm(
            instance=attendance,
            user=request.user
        )

        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        attendance = get_object_or_404(
            StudentAttendance,
            pk=pk,
            faculty=request.user
        )

        form = StudentAttendanceForm(
            request.POST,
            instance=attendance,
            user=request.user
        )

        if form.is_valid():
            updated = form.save(commit=False)
            updated.faculty = request.user  # 🔐 safety
            updated.save()

            messages.success(request, "Attendance updated successfully.")
            return redirect('faculty:attendance-list')

        return render(request, self.template_name, {'form': form})

class StudentAttendanceDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        attendance = get_object_or_404(
            StudentAttendance,
            pk=pk,
            faculty=request.user   # 🔐 restrict ownership
        )

        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")
        return redirect('faculty:attendance-list')


         
class FacultyStudentListView(LoginRequiredMixin, View):
    template_name = "student_list.html"

    def get(self, request):

        faculty = request.user

        # Assigned batches & courses
        assignments = FacultyAssignment.objects.filter(
            faculty=faculty
        ).select_related("course", "batch")

        assigned_batch_ids = assignments.values_list("batch_id", flat=True)
        assigned_course_ids = assignments.values_list("course_id", flat=True)

        selected_batch = request.GET.get("batch")
        selected_course = request.GET.get("course")

        # Base queryset → all students assigned to this faculty
        student_assignments = Assignstudent.objects.filter(
            batch_id__in=assigned_batch_ids,
            course_id__in=assigned_course_ids
        ).select_related("student")

        # Apply filters only if selected
        if selected_batch:
            student_assignments = student_assignments.filter(
                batch_id=selected_batch
            )

        if selected_course:
            student_assignments = student_assignments.filter(
                course_id=selected_course
            )

        students = []

        for assign in student_assignments:
            student = assign.student

            total_classes = StudentAttendance.objects.filter(
                student=student,
                batch_id=assign.batch_id
            ).count()

            present_classes = StudentAttendance.objects.filter(
                student=student,
                batch_id=assign.batch_id,
                status="Present"
            ).count()

            attendance_percentage = 0
            if total_classes > 0:
                attendance_percentage = round(
                    (present_classes / total_classes) * 100, 2
                )

            students.append({
                "name": student.name,
                "email": student.email,
                "phone": student.phone_number,
                "attendance": attendance_percentage,
            })

        context = {
            "assignments": assignments,
            "students": students,
            "selected_batch": selected_batch,
            "selected_course": selected_course,
        }

        return render(request, self.template_name, context)

        
class FacultyTrainingProgressView(LoginRequiredMixin, View):
    template_name = "training_progress.html"

    def get(self, request):
        status_filter = request.GET.get("status")

        # Only logged-in faculty sessions
        sessions = TrainingSession.objects.filter(
            faculty=request.user,
            approval_status="Approved"
        ).select_related("batch")

        # Filter by status if selected
        if status_filter in ["Ongoing", "Completed"]:
            sessions = sessions.filter(status=status_filter)

        context = {
            "sessions": sessions,
            "status_filter": status_filter,
        }

        return render(request, self.template_name, context)

class FacultyReportCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "report_form.html"

    # 🔐 Role Check
    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and
            user.role and
            user.role.role_name.lower() == "faculty"
        )

    # 🚫 If Not Authorized
    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to access this page.")
        return redirect("users:login")

    def get(self, request):
        form = FacultyDailyReportForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = FacultyDailyReportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.faculty = request.user
            report.save()

            messages.success(request, "Report created successfully.")
            return redirect("faculty:faculty_report_list")

        return render(request, self.template_name, {"form": form})


class FacultyReportListView(LoginRequiredMixin, View):
    template_name = "report_list.html"

    def get(self, request):
        reports = FacultyDailyReport.objects.filter(
            faculty=request.user
        )
        return render(request, self.template_name, {"reports": reports})

class FacultyReportUpdateView(LoginRequiredMixin, View):
    template_name = "report_form.html"

    def get(self, request, pk):
        report = get_object_or_404(
            FacultyDailyReport,
            pk=pk,
            faculty=request.user
        )
        form = FacultyDailyReportForm(instance=report)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        report = get_object_or_404(
            FacultyDailyReport,
            pk=pk,
            faculty=request.user
        )
        form = FacultyDailyReportForm(request.POST, instance=report)

        if form.is_valid():
            updated_report = form.save(commit=False)
            updated_report.faculty = request.user
            updated_report.save()

            messages.success(request, "Report updated successfully.")
            return redirect("faculty:faculty_report_list")

        return render(request, self.template_name, {"form": form})

class FacultyReportDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        report = get_object_or_404(
            FacultyDailyReport,
            pk=pk,
            faculty=request.user
        )
        report.delete()
        messages.success(request, "Report deleted successfully.")
        return redirect("faculty:faculty_report_list")

class Home1View(View):
    def get(self, request):
        return render(request, "home.html")  