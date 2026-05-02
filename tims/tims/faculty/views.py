
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import now
from tims.adminapp.models import LeaveAllocation, LeaveApplication, LeaveBalance, LeaveType
from tims.faculty.forms import LeaveApplicationForm
from django.views import View


from datetime import date

from datetime import datetime
from django.utils.timezone import now
from django.contrib import messages
from tims.adminapp.models import LeaveApplication, LeaveBalance, LeaveType
from datetime import date
class ApplyLeaveView(LoginRequiredMixin, View):

    template_name = "faculty/apply_leave.html"

    def get(self, request):

        form = LeaveApplicationForm(user=request.user)

        leave_balances = LeaveBalance.objects.filter(
            user=request.user,
            year=date.today().year
        ).select_related("leave_type")

        total_remaining = sum(b.remaining_days for b in leave_balances)

        return render(request, self.template_name, {
            "form": form,
            "leave_balances": leave_balances,
            "total_remaining": total_remaining,
            "today": date.today(),
        })


    def post(self, request):

        form = LeaveApplicationForm(
            request.POST,
            user=request.user
        )

        form.instance.user = request.user

        if form.is_valid():

            leave = form.save(commit=False)
            leave.user = request.user

            # ✅ SAME calculation
            if leave.day_type == "HALF":
                leave.total_days = 0.5
            else:
                leave.total_days = (leave.end_date - leave.start_date).days + 1

            # ✅ USE MODEL LOGIC (IMPORTANT)
            leave.clean()

            # =========================
            # ✅ CONFIRM CLICKED
            # =========================
            if "confirm" in request.POST:
                leave.save()
                messages.success(request, "Leave applied with LOP.")
                return redirect("faculty:faculty_my_leaves")

            # =========================
            # ✅ SHOW WARNING
            # =========================
            if leave.lop_days > 0:

                leave_balances = LeaveBalance.objects.filter(
                    user=request.user,
                    year=date.today().year
                ).select_related("leave_type")

                total_remaining = sum(b.remaining_days for b in leave_balances)

                return render(request, self.template_name, {
                    "form": form,
                    "leave_balances": leave_balances,
                    "total_remaining": total_remaining,
                    "show_lop_warning": True,
                    "total_days": leave.total_days,
                    "lop_days": leave.lop_days,
                    "normal_days": leave.total_days - leave.lop_days,
                    "today": date.today(),
                })

            # =========================
            # ✅ NORMAL SAVE
            # =========================
            leave.save()
            messages.success(request, "Leave applied successfully.")
            return redirect("faculty:faculty_my_leaves")

        # ❌ INVALID FORM
        leave_balances = LeaveBalance.objects.filter(
            user=request.user,
            year=date.today().year
        )

        total_remaining = sum(b.remaining_days for b in leave_balances)

        return render(request, self.template_name, {
            "form": form,
            "leave_balances": leave_balances,
            "total_remaining": total_remaining,
            "today": date.today(),
        })
    
class MyLeavesView(LoginRequiredMixin, ListView):

    model = LeaveApplication
    template_name = "faculty/my_leaves.html"
    context_object_name = "leaves"

    def get_queryset(self):

        return LeaveApplication.objects.filter(
            user=self.request.user
        ).select_related("leave_type").order_by("-applied_at")
    
class DeleteLeaveView(LoginRequiredMixin, View):

    def get(self, request, leave_id):

        leave = LeaveApplication.objects.filter(
            id=leave_id,
            user=request.user,
            status="Pending"
        ).first()

        if leave:
            leave.delete()
            messages.info(request,"Pending leave deleted.")

        return redirect("faculty:faculty_my_leaves")
    
class FacultyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "fahome.html"

from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from tims.adminapp.models import LeaveApplication
from django.http import JsonResponse



from django.http import JsonResponse


class LeaveCalendarDataView(LoginRequiredMixin, View):

    def get(self, request):

        leaves = (
            LeaveApplication.objects
            .select_related("leave_type")
            .filter(
                user=request.user,
                status__in=["Pending", "Approved"]
            )
            .order_by("status")
        )

        events = []

        for leave in leaves:
            events.append({
                "title": f"{leave.leave_type.name} ({leave.status})",
                "start": leave.start_date,
                "end": leave.end_date,
                "status": leave.status,
            })

        return JsonResponse(events, safe=False)



        return redirect("faculty_my_leaves")
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from tims.faculty.models import TrainingSession,StudentAttendance,FacultyDailyReport,BatchCompletionRequest
from django.contrib.auth import get_user_model
User = get_user_model()
from tims.adminapp.models import Batch, FacultyAssignment, Admission
from tims.faculty.forms import TrainingSessionForm,AttendanceFilterForm,FacultyDailyReportForm, BatchCompletionRequestForm


def resolve_admission_students(admissions):
    admission_list = list(admissions)
    admission_phones = {
        admission.phone
        for admission in admission_list
        if admission.phone
    }

    student_users = User.objects.filter(role__role_name__iexact="Student")

    students_by_phone = {
        user.phone_number: user
        for user in student_users.filter(phone_number__in=admission_phones)
        if user.phone_number
    }
    students_by_username = {
        user.username: user
        for user in student_users.filter(username__in=admission_phones)
    }

    resolved_rows = []
    for admission in admission_list:
        student = (
            students_by_phone.get(admission.phone)
            or students_by_username.get(admission.phone)
        )
        if student:
            resolved_rows.append({
                "admission": admission,
                "student": student,
            })

    return resolved_rows


class TrainingSessionCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'create_session.html'

    # Faculty Role Check
    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and
            user.role and
            user.role.role_name.lower() == "faculty"
        )

    # If Not Authorized
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
        batch_id = request.GET.get("batch")
        session_date = request.GET.get("session_date")

        sessions = TrainingSession.objects.filter(
            faculty=request.user
        ).select_related("batch").order_by('-session_date')

        if batch_id:
            sessions = sessions.filter(batch_id=batch_id)

        if session_date:
            sessions = sessions.filter(session_date=session_date)

        batches = Batch.objects.filter(
            trainingsession__faculty=request.user
        ).distinct()

        context = {
            "sessions": sessions,
            "batches": batches,
            "selected_batch": batch_id,
            "selected_date": session_date,
        }

        return render(request, self.template_name, context)


class TrainingSessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'create_session.html'

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

    def get_assigned_batches(self, user):
        return Batch.objects.filter(
            id__in=FacultyAssignment.objects.filter(
                faculty=user
            ).values_list('batch', flat=True)
        )

    def get(self, request, pk):
        session = get_object_or_404(
            TrainingSession,
            pk=pk,
            faculty=request.user
        )

        form = TrainingSessionForm(instance=session)
        form.fields['batch'].queryset = self.get_assigned_batches(request.user)

        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        session = get_object_or_404(
            TrainingSession,
            pk=pk,
            faculty=request.user
        )

        form = TrainingSessionForm(request.POST, instance=session)
        form.fields['batch'].queryset = self.get_assigned_batches(request.user)

        if form.is_valid():
            try:
                updated_session = form.save(commit=False)
                updated_session.faculty = request.user
                updated_session.save()
                return redirect('faculty:training_list')
            except IntegrityError:
                form.add_error(None, "Duplicate session for this batch on this date.")

        return render(request, self.template_name, {'form': form})


class TrainingSessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

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

    def post(self, request, pk):
        session = get_object_or_404(
            TrainingSession,
            pk=pk,
            faculty=request.user
        )

        session.delete()
        return redirect('faculty:training_list')


class StudentAttendanceCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "attendance_table.html"

    def test_func(self):
        return (
            self.request.user.is_authenticated and
            self.request.user.role and
            self.request.user.role.role_name.lower() == "faculty"
        )

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized.")
        return redirect("users:login")

    def get_admission_rows(self, batch):
        admissions = Admission.objects.filter(
            batch=batch
        ).select_related("enquiry", "batch", "course")
        return resolve_admission_students(admissions)

    def get(self, request):
        form = AttendanceFilterForm(request.GET or None, user=request.user)

        students = None
        existing_attendance = []

        if form.is_valid():
            batch = form.cleaned_data['batch']
            date = form.cleaned_data['date']

            # 🔐 Security check
            if not Batch.objects.filter(
                facultyassignment__faculty=request.user,
                id=batch.id
            ).exists():
                messages.error(request, "Invalid batch selection")
                return redirect("faculty:attendance-create")

            students = self.get_admission_rows(batch)

            existing_attendance = StudentAttendance.objects.filter(
                batch=batch,
                attendance_date=date
            ).values_list('student_id', flat=True)

        return render(request, self.template_name, {
            "form": form,
            "students": students,
            "existing_attendance": existing_attendance
        })

    def post(self, request):
        form = AttendanceFilterForm(request.POST, user=request.user)

        if form.is_valid():
            batch = form.cleaned_data['batch']
            date = form.cleaned_data['date']

            # 🔐 Security check
            if not Batch.objects.filter(
                facultyassignment__faculty=request.user,
                id=batch.id
            ).exists():
                messages.error(request, "Invalid batch selection")
                return redirect("faculty:attendance-create")

            admission_rows = self.get_admission_rows(batch)

            for row in admission_rows:
                student = row["student"]
                present = request.POST.get(f"student_{student.id}") == "on"

                StudentAttendance.objects.update_or_create(
                    student=student,
                    attendance_date=date,
                    defaults={
                        "batch": batch,
                        "faculty": request.user,
                        "is_present": present
                    }
                )

            messages.success(request, "Attendance saved successfully")
            return redirect("faculty:attendance-create")

        return render(request, self.template_name, {"form": form})
         
         
class FacultyStudentListView(LoginRequiredMixin, View):
    template_name = "student_list.html"

    def get(self, request):

        faculty = request.user

        # ✅ Assigned batches & courses
        assignments = FacultyAssignment.objects.filter(
            faculty=faculty
        ).select_related("course", "batch")

        assigned_batch_ids = assignments.values_list("batch_id", flat=True)
        assigned_course_ids = assignments.values_list("course_id", flat=True)

        selected_batch = request.GET.get("batch")
        selected_course = request.GET.get("course")

        student_admissions = Admission.objects.filter(
            batch_id__in=assigned_batch_ids,
            course_id__in=assigned_course_ids
        ).select_related("enquiry", "batch", "course")

        # ✅ Apply filters
        if selected_batch:
            student_admissions = student_admissions.filter(batch_id=selected_batch)

        if selected_course:
            student_admissions = student_admissions.filter(course_id=selected_course)

        students = []
        for row in resolve_admission_students(student_admissions):
            admission = row["admission"]
            student = row["student"]
            batch = admission.batch

            # ✅ Total classes
            total_classes = StudentAttendance.objects.filter(
                student=student,
                batch=batch
            ).count()

            # ✅ Present classes
            present_classes = StudentAttendance.objects.filter(
                student=student,
                batch=batch,
                is_present=True   # ✅ FIXED
            ).count()

            attendance_percentage = 0
            if total_classes > 0:
                attendance_percentage = round(
                    (present_classes / total_classes) * 100, 2
                )

            students.append({
                "name": student.name,
                "email": student.email,
                "phone": getattr(student, "phone_number", ""),  # safe
                "attendance": attendance_percentage,
                "batch": batch.batch_name,
                "course": admission.course.course_name,
            })

        context = {
            "assignments": assignments,
            "students": students,
            "selected_batch": selected_batch,
            "selected_course": selected_course,
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
        return render(request, "fahome.html")  
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from tims.adminapp.models import FacultyAssignment
from tims.faculty.forms import FacultyCourseMaterialForm

class FacultyMaterialAddView(View):
    template_name = "course_material_form.html"

    def get(self, request):
        form = FacultyCourseMaterialForm(faculty=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = FacultyCourseMaterialForm(request.POST, request.FILES, faculty=request.user)
        if form.is_valid():
            material = form.save(commit=False)
            material.faculty = request.user  # assign logged-in faculty
            material.save()
            return redirect("faculty:material_add")  # redirect back to add page or list
        return render(request, self.template_name, {"form": form})

from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from tims.adminapp.models import LeaveApplication
from tims.faculty.models import TrainingSession, StudentAttendance

class Home1View(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user

        # 🔹 Leaves
        total_leaves = LeaveApplication.objects.filter(user=user).count()
        pending_leaves = LeaveApplication.objects.filter(user=user, status="Pending").count()
        approved_leaves = LeaveApplication.objects.filter(user=user, status="Approved").count()

        # 🔹 Training Sessions
        total_sessions = TrainingSession.objects.filter(faculty=user).count()

        # 🔹 Attendance
        total_attendance = StudentAttendance.objects.filter(faculty=user).count()

        # 🔹 Recent Leaves
        recent_leaves = LeaveApplication.objects.filter(user=user).order_by("-applied_at")[:5]

        context = {
            "total_leaves": total_leaves,
            "pending_leaves": pending_leaves,
            "approved_leaves": approved_leaves,
            "total_sessions": total_sessions,
            "total_attendance": total_attendance,
            "recent_leaves": recent_leaves,
        }

        return render(request, "fahome.html", context)

class FacultyBatchCompletionRequestCreateView(LoginRequiredMixin, View):
    template_name = "faculty_completion_request_form.html"

    def get(self, request):
        form = BatchCompletionRequestForm(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = BatchCompletionRequestForm(request.POST, user=request.user)

        batch_id = request.POST.get("batch")
        if batch_id:
            selected_batch = Batch.objects.filter(
                id=batch_id,
                facultyassignment__faculty=request.user
            ).distinct().first()

            if selected_batch and selected_batch.end_date and selected_batch.end_date > timezone.localdate():
                form.add_error(
                    "requested_completion_date",
                    f"Completion request can only be submitted on or after the batch end date ({selected_batch.end_date})."
                )
                return render(request, self.template_name, {"form": form})

        if form.is_valid():
            completion_request = form.save(commit=False)
            completion_request.faculty = request.user
            completion_request.course = completion_request.batch.course
            try:
                completion_request.full_clean()
            except ValidationError as exc:
                for field, errors in exc.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != "__all__" else None, error)
                return render(request, self.template_name, {"form": form})
            completion_request.save()

            messages.success(request, "Completion request submitted successfully.")
            return redirect("faculty:completion-request-list")

        return render(request, self.template_name, {"form": form})

class FacultyBatchCompletionRequestListView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "faculty_completion_request_list.html"

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
        status = request.GET.get("status")
        batch_id = request.GET.get("batch")

        requests_qs = BatchCompletionRequest.objects.filter(
            faculty=request.user
        ).select_related("batch", "course").order_by("-requested_at")

        if status:
            requests_qs = requests_qs.filter(status=status)

        if batch_id:
            requests_qs = requests_qs.filter(batch_id=batch_id)

        assigned_batch_ids = FacultyAssignment.objects.filter(
            faculty=request.user
        ).values_list("batch_id", flat=True)

        batches = Batch.objects.filter(id__in=assigned_batch_ids)

        context = {
            "requests_qs": requests_qs,
            "batches": batches,
            "selected_status": status,
            "selected_batch": batch_id,
        }

        return render(request, self.template_name, context)

class FacultyBatchCompletionRequestDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

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

    def post(self, request, pk):
        completion_request = get_object_or_404(
            BatchCompletionRequest,
            pk=pk,
            faculty=request.user
        )

        if completion_request.status != "Pending":
            messages.error(request, "Only pending requests can be deleted.")
            return redirect("faculty:completion-request-list")

        completion_request.delete()
        messages.success(request, "Completion request deleted successfully.")
        return redirect("faculty:completion-request-list")        
