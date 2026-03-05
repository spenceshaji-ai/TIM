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
from django.utils.timezone import now
from django.db.models import OuterRef, Subquery
import secrets

from tims.adminapp.models import Course, Batch, Enquiry, FollowUp, Admission,Payment
from .forms import CourseForm, BatchForm, EnquiryForm, FollowUpForm, AdmissionForm,PaymentForm
from datetime import date

from tims.adminapp.models import FacultyAssignment,Assignstudent
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import FacultyAssignmentForm,AssignstudentForm
from django.contrib import messages
from django.db import models
from django.db.models import Sum
from tims.users.models import Role,User
from django.contrib import messages



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
        # 🔥 Attach next follow-up date from FollowUp table
        for enquiry in enquiries:
            last_followup = FollowUp.objects.filter(
                enquiry=enquiry
            ).order_by("-id").first()   # latest followup

            
            if last_followup and last_followup.next_followup_date:
                enquiry.next_followup_date = last_followup.next_followup_date
        
        return render(request, self.template_name, {
               "enquiries": enquiries,
               "today": date.today(),   # ⭐ REQUIRED
        })

class EnquiryCreateView(View):
    template_name = "enquiry/enquiry_form.html"

    def get(self, request):
        form = EnquiryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EnquiryForm(request.POST)

        if form.is_valid():
            enquiry=form.save()
             # 🔥 Create FollowUp automatically if date exists
            if enquiry.next_followup_date:
                FollowUp.objects.create(
                    enquiry=enquiry,
                    followup_date=enquiry.next_followup_date,
                    status="Pending"   # or any default
                )
            

            return redirect("adminapp:enquiry_list")

        return render(request, self.template_name, {"form": form})



class EnquiryDetailView(View):
    template_name = "enquiry/enquiry_detail.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)

        followups = FollowUp.objects.filter(
            enquiry=enquiry
        ).order_by("-followup_date")   # 🔥 newest date first

        return render(request, self.template_name, {
            "enquiry": enquiry,
            "followups": followups
        })


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
            return redirect("adminapp:enquiry_list")

        return render(request, self.template_name, {"form": form})

class EnquiryDeleteView(View):
    template_name = "enquiry/enquiry_delete.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        return render(request, self.template_name, {"enquiry": enquiry})

    def post(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        enquiry.delete()
        return redirect("adminapp:enquiry_list")
    
class MarkNotInterestedView(View):

    def get(self, request, enquiry_id):
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        enquiry.status = "Not Interested"
        enquiry.save()

        return redirect("adminapp:enquiry_detail", pk=enquiry.id)

    
#FOLLOWUP
class FollowUpCreateView(View):
    template_name = "followup/followup_form.html"

    def get(self, request, enquiry_id):
        
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        form = FollowUpForm(initial={
            "followup_date": enquiry.next_followup_date
        })
        
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
            followup.created_by = request.user

            followup.save()
            # 👇 Update enquiry's next follow-up date
            enquiry.next_followup_date = followup.next_followup_date
            enquiry.save()

            return redirect("adminapp:""enquiry_detail", pk=enquiry.id)

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })
class FollowUpListView(View):
    template_name = "followup/followup_list.html"

    def get(self, request, enquiry_id):
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        followups = FollowUp.objects.filter(
            enquiry=enquiry
        ).order_by("-followup_date")   # 🔥 Feb 20 first

        return render(request, self.template_name, {
            
            "followups": followups,
            "enquiry": enquiry
        })
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import FollowUp
from .forms import FollowUpForm


class FollowUpUpdateView(View):
    template_name = "followup/followup_form.html"

    def get(self, request, pk):
        followup = get_object_or_404(FollowUp, id=pk)
        form = FollowUpForm(instance=followup)

        return render(request, self.template_name, {
            "form": form,
            "followup": followup,
            "enquiry":followup.enquiry
        })

    def post(self, request, pk):
        followup = get_object_or_404(FollowUp, id=pk)
        form = FollowUpForm(request.POST, instance=followup)

        if form.is_valid():
            form.save()

            # 🔥 Go back to enquiry detail page
            return redirect("adminapp:enquiry_detail", followup.enquiry_id)

        return render(request, self.template_name, {
            "form": form,
            "followup": followup,
            "enquiry":followup.enquiry
        })
class ConvertToAdmissionView(View):
    template_name = "admission/admission_form.html"

    def get(self, request, enquiry_id):

        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        # ✅ Pre-fill data from Enquiry
        form = AdmissionForm(initial={
            "student_name": enquiry.name,
            "phone": enquiry.phone,
            "email": enquiry.email,
            "course": enquiry.course,
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

            return redirect("adminapp:admission_list")

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })

class AdmissionListView(View):
    template_name = "admission/admission_list.html"

    def get(self, request):

        admissions = Admission.objects.all().order_by("-admission_date")

        for adm in admissions:
            paid = adm.payments.aggregate(
                total=models.Sum("amount")
            )["total"] or 0

            adm.paid_amount = paid
            adm.pending_amount = adm.course.fee - paid

        # ⭐ ADD THIS HERE
        users_usernames = list(
            User.objects.values_list("username", flat=True)
        )

        return render(request, self.template_name, {
            "admissions": admissions,
            "users_usernames": users_usernames   # ⭐ PASS TO TEMPLATE
        })



class CreateStudentAccountView(View):

    def post(self, request, admission_id):

        # 🔐 Allow only Admin
        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("adminapp:admission_list")

        admission = get_object_or_404(Admission, id=admission_id)
        enquiry = admission.enquiry

        # ⭐ Correct role name
        student_role = Role.objects.get(role_name="Student")

        # ⭐ Check if already registered
        existing_user = User.objects.filter(username=enquiry.phone).first()

        if existing_user:
            messages.info(request, "Student already registered")
            return redirect("adminapp:admission_list")
        
        # ⭐ Generate random password
        temp_password = secrets.token_urlsafe(8)
        
        # ⭐ Create new account
        User.objects.create_user(
            username=enquiry.phone,
            email=enquiry.email or "",
            password=temp_password,
            role=student_role,
            name=enquiry.name,
            phone_number=enquiry.phone,
            must_change_password=True
            
        )

        enquiry.status = "Converted"
        enquiry.save()

         # ⭐ Show password to admin
        messages.success(
            request,
            f"Student registered successfully. Temporary password: {temp_password}"
        )

        return redirect("adminapp:admission_list")
    



# -----------------------------
# Payment Create View
# -----------------------------


class PaymentCreateView(View):


     # 👉 Show form + admission fee data
    def get(self, request):

        form = PaymentForm()

        admissions = Admission.objects.select_related("course").all()

        admission_data = []

        for adm in admissions:
            total_fee = adm.course.fee

            paid_total = adm.payments.aggregate(
                total=Sum("amount")
            )["total"] or 0

            admission_data.append({
                "id": adm.id,
                "fee": float(total_fee),
                "paid": float(paid_total),
            })

        return render(
            request,
            "payment/payment_form.html",
            {
                "form": form,
                "admission_data": admission_data   # ⭐ MUST send this
            }
        )

    

    def post(self, request):
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)

            admission = payment.admission
            total_fee = admission.course.fee

            paid_total = admission.payments.aggregate(
                total=Sum("amount")
            )["total"] or 0

            new_amount = payment.amount

            # 🚨 VALIDATION
            if paid_total >= total_fee:
                form.add_error(None, "Fees already fully paid.")
                return render(request, "payment/payment_form.html", {"form": form})

            if paid_total + new_amount > total_fee:
                remaining = total_fee - paid_total
                form.add_error(
                    "amount",
                    f"Amount exceeds pending fee. Remaining: {remaining}"
                )
                return render(request, "payment/payment_form.html", {"form": form})

            payment.save()
            return redirect("adminapp:payment_list")

        return render(request, "payment/payment_form.html", {"form": form})



# -----------------------------
# Payment List View
# -----------------------------
class PaymentListView(View):

    def get(self, request):
        payments = Payment.objects.select_related("admission").all()
        # 🔥 Add calculations for each payment row
        for p in payments:

            total_fee = p.admission.course.fee   # Total course fee

            paid = p.admission.payments.aggregate(
                total=Sum("amount")
            )["total"] or 0   # Total paid so far

            p.total_fee = total_fee
            p.paid_amount = paid
            p.pending_fee = total_fee - paid

        return render(
            request,
            "payment/payment_list.html",
            {"payments": payments}
        )

class PaymentUpdateView(View):
    template_name = "payment/payment_form.html"

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        form = PaymentForm(instance=payment)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        form = PaymentForm(request.POST, instance=payment)

        if form.is_valid():
            form.save()
            return redirect("adminapp:payment_list")

        return render(request, self.template_name, {"form": form})


class PaymentDeleteView(View):

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return redirect("adminapp:payment_list")



class FacultyAssignmentCreateView(View):
    template_name = "faculty_assignment.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": FacultyAssignmentForm()
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

class Home2View(View):
    def get(self, request):
        return render(request, "pages/adminhome.html")


from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()





class StaffListCreateView(View):
    template_name = "staff_list.html"

    # ✅ Show page
    def get(self, request):

        if not request.user.is_superuser:
            return redirect("login")

        staff = User.objects.filter(
            role__role_name__in=["Admin", "HR", "Manager"]
        )

        roles = Role.objects.filter(
            role_name__in=["Admin", "HR", "Manager"]
        )

        return render(request, self.template_name, {
            "staff": staff,
            "roles": roles
        })

    # ✅ Handle form submit
    def post(self, request):

        if not request.user.is_superuser:
            return redirect("login")

        role_id = request.POST.get("role")   # 🔥 get role ID
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        status = request.POST.get("status")

        if not all([role_id, name, username, phone, password]):
            messages.error(request, "All required fields must be filled")
            return redirect("adminapp:staff_list")

    # ✅ Get role using ID
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            messages.error(request, "Invalid role selected")
            return redirect("adminapp:staff_list")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("adminapp:staff_list")

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect("adminapp:staff_list")

        user = User.objects.create(
            username=username,
            name=name,
            email=email,
            phone_number=phone,
            role=role,
            status=status,
            is_staff=True,
            must_change_password=True 
    )

        user.set_password(password)
        user.save()

        messages.success(request, f"{role.role_name} created successfully")
        return redirect("adminapp:staff_list") 

class EditStaffView(View):
    template_name = "edit_staff.html"
    def get(self, request, pk):
        staff = get_object_or_404(User, pk=pk)
        roles = Role.objects.all()

        return render(request, self.template_name, {
            "staff": staff,
            "roles": roles
        })

    def post(self, request, pk=None):
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = User()
        user = User.objects.get(pk=pk)
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.status = request.POST.get("status")
        user.save()
        return redirect("adminapp:staff_list")


class DeleteStaffView(View):

    def post(self, request, pk):

        if not request.user.is_superuser:
            return redirect("login")

        staff = get_object_or_404(User, pk=pk)
        staff.delete()

        return redirect("adminapp:staff_list")

class FacultyListCreateView(View):
    template_name = "faculty_list.html"

    # ✅ Show page
    def get(self, request):
        print("Authenticated:", request.user.is_authenticated)
        print("User:", request.user)
        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")

        faculty = User.objects.filter(role__role_name="Faculty")

        return render(request, self.template_name, {
            "faculty": faculty
        })

    # ✅ Handle form submit
    def post(self, request):


        


        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if not all([name, phone, password]):
            messages.error(request, "All required fields must be filled")
            return redirect("adminapp:faculty_list")

        faculty_role = Role.objects.filter(role_name="Faculty").first()
         # ✅ phone duplicate validation
        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already registered")
            return redirect("adminapp:faculty_list")

        if not faculty_role:
            messages.error(request, "Faculty role not found")
            return redirect("adminapp:faculty_list")

        if User.objects.filter(username=phone).exists():
            messages.error(request, "Faculty already exists")
            return redirect("adminapp:faculty_list")

        User.objects.create_user(
            username=username,
            password=password,
            name=name,
            email=email,
            phone_number=phone,
            role=faculty_role,
            status="active"
        )

        messages.success(request, "Faculty created successfully")
        return redirect("adminapp:faculty_list")

class EditFacultyView(View):
    template_name = "edit_faculty.html"

    def get(self, request, pk):

        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")

        faculty = User.objects.get(id=pk)

        return render(request, self.template_name, {
            "faculty": faculty
        })

    def post(self, request, pk):

        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")

        faculty = User.objects.get(id=pk)

        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        status = request.POST.get("status")

        # username validation
        if User.objects.exclude(id=faculty.id).filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("adminapp:edit_faculty", pk=pk)

        # phone validation
        if User.objects.exclude(id=faculty.id).filter(phone_number=phone).exists():
            messages.error(request, "Phone number already registered")
            return redirect("adminapp:edit_faculty", pk=pk)

        faculty.name = name
        faculty.username = username
        faculty.email = email
        faculty.phone_number = phone
        faculty.status = status

        faculty.save()

        messages.success(request, "Faculty updated successfully")

        return redirect("adminapp:faculty_list")
    
class DeleteFacultyView(View):

    def post(self, request, pk):

        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")

        faculty = User.objects.get(id=pk)

        faculty.delete()

        messages.success(request, "Faculty deleted successfully")

        return redirect("adminapp:faculty_list")