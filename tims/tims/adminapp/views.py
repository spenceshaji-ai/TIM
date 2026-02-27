from django.views.generic import ListView, View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse

from tims.conftest import user
User = get_user_model()
from adminapp.models import LeaveApplication, Salary
from django.db.models import Case, When, Value, IntegerField
from adminapp.forms import LeaveBalanceForm
from datetime import date
from decimal import Decimal
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from datetime import date
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
from datetime import date

from django.contrib.auth import get_user_model
User = get_user_model()

from adminapp.models import (
    LeaveApplication,
    LeaveBalance,
    LeaveAllocation,
    LeaveType,
    monthly_accrual,
    yearly_leave_reset
)

def is_superadmin(user):
    return user.is_superuser

# HR
def is_hr(user):
    return hasattr(user, "role") and user.role.role_name == "HR"

# Admin
def is_admin(user):
    return hasattr(user, "role") and user.role.role_name == "Admin"

# Manager
def is_manager(user):
    return hasattr(user, "role") and user.role.role_name == "Manager"

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "pages/home.html"


from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from adminapp.models import Salary, Holiday
from adminapp.forms import SalaryForm, HolidayForm

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ValidationError

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.timezone import now

class LeaveUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "adminapp/leave_users.html"
    context_object_name = "users"

    def test_func(self):
        return self.request.user.is_superuser or (
            hasattr(self.request.user, "role") and
            self.request.user.role.role_name == "HR"
        )

    def get_queryset(self):
        queryset = User.objects.all().order_by("username")

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(username__icontains=search)

        return queryset
# =====================================================
# 1️⃣ SALARY USERS PAGE (LIKE LEAVE USERS)
# =====================================================

class SalaryUsersView(ListView):
    model = User
    template_name = "adminapp/salary_users.html"
    context_object_name = "users"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(username__icontains=search)

        return queryset


# =====================================================
# 2️⃣ USER-WISE SALARY HISTORY
# =====================================================

class UserSalaryHistoryView(ListView):
    model = Salary
    template_name = "adminapp/user_salary_history.html"
    context_object_name = "salaries"

    def get_queryset(self):
        return Salary.objects.filter(
            faculty_id=self.kwargs["pk"]
        ).order_by("-year", "-month")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_user"] = User.objects.get(id=self.kwargs["pk"])
        return context


# =====================================================
# 3️⃣ ADD SALARY FOR SELECTED USER
# =====================================================

class UserSalaryCreateView(CreateView):
    model = Salary
    form_class = SalaryForm
    template_name = "adminapp/salary_form.html"

    def get_initial(self):
        return {
            "faculty": self.kwargs["pk"],
            "year": now().year
        }

    def form_valid(self, form):
        messages.success(self.request, "Salary Added Successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Salary already exists for this month!")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "adminapp:user_salary_history",
            kwargs={"pk": self.kwargs["pk"]}
        )


# =====================================================
# 4️⃣ UPDATE SALARY
# =====================================================

class SalaryUpdateView(UpdateView):
    model = Salary
    form_class = SalaryForm
    template_name = "adminapp/salary_form.html"

    def dispatch(self, request, *args, **kwargs):
        salary = self.get_object()
        if salary.status == "Paid":
            messages.error(request, "Cannot edit. Salary already paid!")
            return redirect("adminapp:user_salary_history", pk=salary.faculty.id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Salary Updated Successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "adminapp:user_salary_history",
            kwargs={"pk": self.object.faculty.id}
        )


# =====================================================
# 5️⃣ DELETE SALARY
# =====================================================

class SalaryDeleteView(DeleteView):
    model = Salary
    template_name = "adminapp/salary_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        salary = self.get_object()
        if salary.status == "Paid":
            messages.error(request, "Cannot delete. Salary already paid!")
            return redirect("adminapp:user_salary_history", pk=salary.faculty.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "adminapp:user_salary_history",
            kwargs={"pk": self.object.faculty.id}
        )


# =====================================================
# 6️⃣ MARK SALARY AS PAID
# =====================================================

class SalaryMarkPaidView(View):
    def post(self, request, pk):
        salary = get_object_or_404(Salary, pk=pk)

        if salary.status == "Paid":
            messages.warning(request, "Salary already marked as paid.")
        else:
            salary.status = "Paid"
            salary.save()
            messages.success(request, "Salary marked as Paid!")

        return redirect("adminapp:user_salary_history", pk=salary.faculty.id)

class HolidayCreateView(CreateView):
    model = Holiday
    form_class = HolidayForm
    template_name = "adminapp/holiday_form.html"
    success_url = reverse_lazy("adminapp:holiday_list")

    def form_valid(self, form):
        messages.success(self.request, "Holiday Added Successfully!")
        return super().form_valid(form)

from django.utils.timezone import now
from django.views.generic import DeleteView

class HolidayDeleteView(DeleteView):
    model = Holiday
    template_name = "adminapp/holiday_confirm_delete.html"
    success_url = reverse_lazy("adminapp:holiday_list")

class HolidayListView(ListView):
    model = Holiday
    template_name = "adminapp/holiday_list.html"
    context_object_name = "holidays"

    def get_queryset(self):
        return Holiday.objects.filter(
            date__gte=now().date()
        ).order_by("date")

class HolidayUpdateView(UpdateView):
    model = Holiday
    form_class = HolidayForm
    template_name = "adminapp/holiday_form.html"
    success_url = reverse_lazy("adminapp:holiday_list")

class LeaveRequestsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LeaveApplication
    template_name = "adminapp/leave_requests.html"
    context_object_name = "leaves"

    def test_func(self):
        user = self.request.user
        return user.is_superuser or (
            hasattr(user, "role") and user.role.role_name == "HR"
        )

    def get_queryset(self):
        return (
            LeaveApplication.objects.select_related("user", "leave_type")
            .annotate(
                status_priority=Case(
                    When(status="Pending", then=Value(1)),
                    When(status="Approved", then=Value(2)),
                    When(status="Rejected", then=Value(3)),
                    output_field=IntegerField(),
                )
            )
            .order_by("status_priority", "-applied_at")
        )
    
from datetime import date
from django.http import HttpResponseForbidden
from adminapp.models import LeaveBalance
from datetime import date
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from adminapp.models import LeaveApplication, LeaveBalance

class UpdateLeaveStatusView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        user = self.request.user
        return user.is_superuser or (
            hasattr(user, "role") and user.role.role_name == "HR"
        )

    def get(self, request, leave_id, status):

        leave = get_object_or_404(LeaveApplication, id=leave_id)

        if leave.status != "Pending":
            messages.warning(request, "Already processed.")
            return redirect("adminapp:leave_requests")

        if status == "Approved":

            year = leave.start_date.year

            balance, created = LeaveBalance.objects.get_or_create(
                user=leave.user,
                leave_type=leave.leave_type,
                year=year,
                defaults={
                    "earned_days": 0,
                    "used_days": 0,
                    "lop_days": 0
                }
            )

            requested_days = leave.total_days
            available_days = balance.remaining_days()

            # 🔥 LOP Logic
            if requested_days <= available_days:
                balance.used_days += requested_days
                leave.lop_days = 0
            else:
                balance.used_days += available_days
                leave.lop_days = requested_days - available_days
                balance.lop_days += leave.lop_days

            balance.save()

        else:
            leave.lop_days = 0

        leave.status = status
        leave.save()

        messages.success(request, f"Leave {status} successfully.")
        return redirect("adminapp:leave_requests")





class LeaveHistoryDetailView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "adminapp/leave_history_detail.html"
    context_object_name = "leaves"

    def test_func(self):
        return self.request.user.is_superuser or (
            hasattr(self.request.user, "role") and
            self.request.user.role.role_name == "HR"
        )

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return LeaveApplication.objects.filter(
            user_id=user_id,
            status="Approved"
        ).select_related("leave_type")

class MonthlyAccrualView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        monthly_accrual()
        messages.success(request, "Monthly leave credited successfully.")
        return redirect("adminapp:leave_requests")
    
class YearlyResetView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        yearly_leave_reset()
        messages.success(request, "Yearly reset completed.")
        return redirect("adminapp:leave_requests")
    
from adminapp.models import LeaveBalance
from datetime import date
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date


class HRLeaveAssignView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser or (
            hasattr(self.request.user, "role") and
            self.request.user.role.role_name == "HR"
        )

    def get(self, request, user_id):
        employee = get_object_or_404(User, id=user_id)
        year = date.today().year

        balances = LeaveBalance.objects.filter(
            user=employee,
            year=year
        ).select_related("leave_type")

        return render(request, "adminapp/hr_leave_assign.html", {
            "employee": employee,
            "leave_types": LeaveType.objects.all(),
            "year": year,
            "balances": balances
        })

    def post(self, request, user_id):
        employee = get_object_or_404(User, id=user_id)
        year = date.today().year

        leave_type_id = request.POST.get("leave_type")
        total_days = request.POST.get("total_days")

        if not leave_type_id or not total_days:
            messages.error(request, "Please select leave type and total days.")
            return redirect("adminapp:hr_leave_assign", user_id=user_id)

        leave_type = get_object_or_404(LeaveType, id=leave_type_id)

        total_days = float(total_days)

        # 1️⃣ Update or Create LeaveAllocation
        LeaveAllocation.objects.update_or_create(
            user=employee,
            leave_type=leave_type,
            year=year,
            defaults={"total_days": total_days}
        )

        # 2️⃣ Update or Create LeaveBalance (DO NOT reset used_days)
        balance, created = LeaveBalance.objects.get_or_create(
            user=employee,
            leave_type=leave_type,
            year=year,
            defaults={
                "earned_days": total_days,
                "used_days": 0,
                "lop_days": 0
            }
        )

        if not created:
            balance.earned_days = total_days
            balance.save()

        messages.success(request, "Leave allocation updated successfully.")
        return redirect("adminapp:hr_leave_assign", user_id=user_id)
class ManagementLeaveApplyView(LoginRequiredMixin, View):
    template_name = "adminapp/management_leave_apply.html"

    def get(self, request):
        form = LeaveApplicationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LeaveApplicationForm(request.POST)

        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.status = "Pending"
            leave.save()
            return redirect("adminapp:management_leave_list")

        return render(request, self.template_name, {"form": form})
    
class ManagementLeaveListView(LoginRequiredMixin, ListView):
    template_name = "adminapp/management_leave_list.html"
    context_object_name = "leaves"

    def get_queryset(self):
        return LeaveApplication.objects.filter(
            user=self.request.user
        ).order_by("-id")

from django.http import JsonResponse

class LeaveCalendarDataView(View):
    def get(self, request):
        leaves = LeaveApplication.objects.select_related(
            "user", "leave_type"
        ).filter(status="Approved")   # ✅ ONLY approved

        events = []
        for leave in leaves:
            events.append({
                "title": f"{leave.user.username} ({leave.leave_type.leave_name})",
                "start": leave.start_date,
                "end": leave.end_date,
                "status": leave.status,
            })

        return JsonResponse(events, safe=False)


    
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from tims.adminapp.forms import CourseForm,BatchForm
from .models import Enquiry, FollowUp
from .forms import EnquiryForm,FollowUpForm
from .models import Admission
from .forms import AdmissionForm
from tims.adminapp.models import Course,Batch,FacultyAssignment,Assignstudent
from tims.faculty.models import TrainingSession,FacultyDailyReport,StudentAttendance
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CourseForm,BatchForm,FacultyAssignmentForm,AssignstudentForm
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_time, parse_datetime

# List
class CourseListView(View):
    template_name = "course_list.html"

    def get(self, request):
        courses = Course.objects.all()
        return render(request, self.template_name, {"courses": courses})

# ADD
class CourseCreateView(View):
    template_name = "course_add.html"

    def get(self, request):
        form = CourseForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:course_list')
        return render(request, self.template_name, {"form": form})

# EDIT
class CourseEditView(View):
    template_name = "course_edit.html"

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        form = CourseForm(instance=course)
        return render(request, self.template_name, {
            "form": form,
            "course": course
        })

    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('adminapp:course_list')
        return render(request, self.template_name, {
            "form": form,
            "course": course
        })

# DELETE (separate page)
class CourseDeleteView(View):

    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        course.delete()
        return redirect('adminapp:course_list')


class BatchCreateView(View):
    template_name="batch_add.html"

    def get(self, request):
        form = BatchForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminapp:batch_list")
        return render(request, self.template_name, {"form": form})

class BatchListView(View):
    template_name="batch_list.html"

    def get(self, request):
        batches = Batch.objects.select_related("course")
        return render(request, self.template_name, {"batches": batches})


class BatchEditView(View):
    template_name = "batch_add.html"

    def get(self, request, id):
        batch = get_object_or_404(Batch, id=id)
        form = BatchForm(instance=batch)
        return render(request, self.template_name, {
            "form": form,
            "batch": batch
        })

    def post(self, request, id):
        batch = get_object_or_404(Batch, id=id)
        form = BatchForm(request.POST, instance=batch)

        if form.is_valid():
            form.save()
            return redirect("adminapp:batch_list")

        return render(request, self.template_name, {
            "form": form,
            "batch": batch
        })

class BatchDeleteView(View):
    def post(self, request, id):
        batch = get_object_or_404(Batch, id=id)
        batch.delete()
        return redirect("batch_list")
    
class EnquiryListView(View):
    template_name = "enquiry/enquiry_list.html"

    def get(self, request):
        enquiries = Enquiry.objects.all().order_by("-created_at")
        return render(request, self.template_name, {"enquiries": enquiries})

class EnquiryCreateView(View):
    template_name = "enquiry/enquiry_form.html"

    def get(self, request):
        form = EnquiryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EnquiryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("enquiry_list")

        return render(request, self.template_name, {"form": form})

class EnquiryDetailView(View):
    template_name = "enquiry/enquiry_detail.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        return render(request, self.template_name, {"enquiry": enquiry})

class EnquiryUpdateView(View):
    template_name = "enquiry/enquiry_form.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        form = EnquiryForm(instance=enquiry)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        form = EnquiryForm(request.POST, instance=enquiry)

        if form.is_valid():
            form.save()
            return redirect("enquiry_list")

        return render(request, self.template_name, {"form": form})

class EnquiryDeleteView(View):
    template_name = "enquiry/enquiry_delete.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        return render(request, self.template_name, {"enquiry": enquiry})

    def post(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        enquiry.delete()
        return redirect("enquiry_list")
    
#FOLLOWUP
class FollowUpCreateView(View):
    template_name = "followup/followup_form.html"

    def get(self, request, enquiry_id):
        form = FollowUpForm()
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })

    def post(self, request, enquiry_id):
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        form = FollowUpForm(request.POST)

        if form.is_valid():
            followup = form.save(commit=False)
            followup.enquiry = enquiry
            followup.save()

            return redirect("enquiry_detail", pk=enquiry.id)

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })
    
class FollowUpListView(View):
    template_name = "followup/followup_list.html"

    def get(self, request):
        followups = FollowUp.objects.all().order_by("-followup_date")
        return render(request, self.template_name, {"followups": followups})


class ConvertToAdmissionView(View):
    template_name = "admission/admission_form.html"

    def get(self, request, enquiry_id):

        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        # ✅ Pre-fill data from Enquiry
        form = AdmissionForm(initial={
            "student_name": enquiry.name,
            "phone": enquiry.phone,
            "email": enquiry.email,
            "course": enquiry.course_id,
        })

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })

    def post(self, request, enquiry_id):

        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        form = AdmissionForm(request.POST)

        if form.is_valid():
            admission = form.save(commit=False)
            admission.enquiry = enquiry
            admission.save()

            # ✅ Update Enquiry Status
            enquiry.status = "Converted"
            enquiry.save()

            return redirect("admission_list")

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })
    
class AdmissionListView(View):
    template_name = "admission/admission_list.html"

    def get(self, request):
        admissions = Admission.objects.all().order_by("-admission_date")
        return render(request, self.template_name, {
            "admissions": admissions
        })

        return redirect("adminapp:batch_list")
    

class FacultyAssignmentCreateView(View):
    template_name = "faculty_assignment.html"

class FacultyAssignmentCreateView(View):
    def get(self, request):
        form = FacultyAssignmentForm()
        return render(request, "adminapp/faculty_assignment.html", {
            "form": form
        })

    def post(self, request):
        form = FacultyAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty assigned successfully")
            return redirect("adminapp:faculty_courses")

        return render(request, self.template_name, {"form": form})

class FacultyCoursesView(View):
    template_name = "facultylist.html"

    def get(self, request):
        faculty_id = request.GET.get("faculty")

        # Only users with Faculty role
        faculties = User.objects.filter(role__role_name="Faculty")

        assignments = None
        if faculty_id:
            assignments = (
                FacultyAssignment.objects
                .filter(faculty_id=faculty_id)
                .select_related("course", "batch")
            )

        return render(request, self.template_name, {
            "faculties": faculties,
            "assignments": assignments,
        })
from django.views.generic import CreateView, ListView, View
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
from tims.adminapp.models import LeaveApplication


class LeaveRequestsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LeaveApplication
    template_name = "adminapp/leave_requests.html"
    context_object_name = "leaves"

    def test_func(self):
        return self.request.user.is_staff


class UpdateLeaveStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, leave_id, status):
        leave = get_object_or_404(LeaveApplication, id=leave_id)
        leave.status = status
        leave.save()
        return redirect("leave_requests")


class LeaveUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "adminapp/leave_users.html"
    context_object_name = "users"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return User.objects.filter(
            leaveapplication__status="Approved"
        ).distinct()


class LeaveHistoryDetailView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LeaveApplication
    template_name = "adminapp/leave_history.html"
    context_object_name = "leaves"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return LeaveApplication.objects.filter(
            user_id=self.kwargs["user_id"],
            status="Approved"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faculty"] = User.objects.get(id=self.kwargs["user_id"])
        return context


class TrainingSessionApprovalListView(View):
    template_name = "training_approval_list.html"

    def get(self, request):
        sessions = TrainingSession.objects.all().order_by('-created_at')
        return render(request, self.template_name, {
            'sessions': sessions
        })

class TrainingSessionApproveView(View):
    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        session.approval_status = 'Approved'
        session.save()
        return redirect('adminapp:admin_training_approval_list')

class TrainingSessionRejectView(View):
    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        session.approval_status = 'Rejected'
        session.save()
        return redirect('adminapp:admin_training_approval_list')


class AssignStudentView(View):
    template_name = "student_assignment.html"

    def get(self, request):
        form = AssignstudentForm()
        assignments = Assignstudent.objects.all()
        return render(request, self.template_name, {
            "form": form,
            "assignments": assignments
        })

    def post(self, request):
        form = AssignstudentForm(request.POST)
        assignments = Assignstudent.objects.all()

        if form.is_valid():
            form.save()
            return redirect("adminapp:assign-student-list")

        return render(request, self.template_name, {
            "form": form,
            "assignments": assignments
        })

class AssignStudentListView(View):
    template_name = "assign_studentlist.html"

    def get(self, request):
        assignments = Assignstudent.objects.select_related(
            "student", "course", "batch"
        )
        return render(request, self.template_name, {
            "assignments": assignments
        })
    
class AssignStudentEditView(View):
    template_name = "student_assignment.html"

    def get(self, request, pk):
        assignment = get_object_or_404(Assignstudent, pk=pk)
        form = AssignstudentForm(instance=assignment)
        return render(request, self.template_name, {
            "form": form,
            "assignment": assignment
        })

    def post(self, request, pk):
        assignment = get_object_or_404(Assignstudent, pk=pk)
        form = AssignstudentForm(request.POST, instance=assignment)

        if form.is_valid():
            form.save()
            return redirect("adminapp:assign-student-list")

        return render(request, self.template_name, {
            "form": form,
            "assignment": assignment
        })

class AssignStudentDeleteView(View):
    def get(self, request, pk):
        assignment = get_object_or_404(Assignstudent, pk=pk)
        assignment.delete()
        return redirect("adminapp:assign-student-list")


class AdminFacultyReportListView(View):
    template_name = "faculty_report_list.html"

    def get(self, request):

        reports = FacultyDailyReport.objects.select_related('faculty')

        # Date filter
        date_filter = request.GET.get('date')

        if date_filter:
            parsed_date = parse_date(date_filter)
            if parsed_date:
                reports = reports.filter(report_date=parsed_date)

        context = {
            "reports": reports,
            "selected_date": date_filter,
        }

        return render(request, self.template_name, context)

class AdminTrainingSessionListView(View):
    template_name = "training_session_list.html"

    def get(self, request):

        sessions = TrainingSession.objects.select_related(
            "faculty", "batch"
        ).all()

        # Filters
        batch_id = request.GET.get("batch")
        faculty_id = request.GET.get("faculty")
        status = request.GET.get("status")

        if batch_id:
            sessions = sessions.filter(batch_id=batch_id)

        if faculty_id:
            sessions = sessions.filter(faculty_id=faculty_id)

        if status:
            sessions = sessions.filter(status=status)

        # Get all batches
        batches = Batch.objects.all()

        # Get only faculty users (role = Faculty)
        faculties = User.objects.filter(role__role_name="Faculty")

        context = {
            "sessions": sessions,
            "batches": batches,
            "faculties": faculties,
            "selected_batch": batch_id,
            "selected_faculty": faculty_id,
            "selected_status": status,
        }

        return render(request, self.template_name, context)

class AssignmentReportView(View):
    template_name = "assignment_report.html"

    def get(self, request):

        course_id = request.GET.get("course")
        batch_id = request.GET.get("batch")
        role_filter = request.GET.get("role")

        users = []

        # ================= STUDENT FILTER =================
        if role_filter == "student":
            assigned_students = Assignstudent.objects.select_related(
                "student", "batch", "batch__course"
            )

            if course_id:
                assigned_students = assigned_students.filter(
                    batch__course_id=course_id
                )

            if batch_id:
                assigned_students = assigned_students.filter(
                    batch_id=batch_id
                )

            for assign in assigned_students:
                user = assign.student

                total = StudentAttendance.objects.filter(
                    student=user
                ).count()

                present = StudentAttendance.objects.filter(
                    student=user,
                    status="Present"
                ).count()

                attendance_percentage = 0
                if total > 0:
                    attendance_percentage = round((present / total) * 100, 2)

                users.append({
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone_number,
                    "attendance": attendance_percentage,
                })

        # ================= FACULTY FILTER =================
        elif role_filter == "faculty":
            assigned_faculty = FacultyAssignment.objects.select_related(
                "faculty", "batch", "batch__course"
            )

            if course_id:
                assigned_faculty = assigned_faculty.filter(
                    batch__course_id=course_id
                )

            if batch_id:
                assigned_faculty = assigned_faculty.filter(
                    batch_id=batch_id
                )

            for assign in assigned_faculty:
                user = assign.faculty

                users.append({
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone_number,
                    "attendance": None,
                })

        context = {
            "courses": Course.objects.all(),
            "batches": Batch.objects.all(),
            "report_data": users,
            "selected_course": course_id,
            "selected_batch": batch_id,
            "selected_role": role_filter,
        }

        return render(request, self.template_name, context)
