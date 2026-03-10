from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import date, datetime

from adminapp.models import LeaveApplication, LeaveBalance, LeaveType


from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from datetime import date
from django.contrib import messages

from adminapp.models import LeaveBalance
from .forms import LeaveApplicationForm


class ApplyLeaveView(LoginRequiredMixin, View):

    template_name = "faculty/apply_leave.html"

    def get(self, request):

        form = LeaveApplicationForm()

        leave_balances = LeaveBalance.objects.filter(
            user=request.user,
            year=date.today().year
        ).select_related("leave_type")

        return render(request, self.template_name, {
            "form": form,
            "leave_balances": leave_balances,
            "today": date.today(),
        })


    def post(self, request):

        form = LeaveApplicationForm(request.POST, user=request.user)

        # ⭐ attach user BEFORE validation
        form.instance.user = request.user

        if form.is_valid():

            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()

            messages.success(request, "Leave request submitted successfully.")

            return redirect("faculty:faculty_my_leaves")

        leave_balances = LeaveBalance.objects.filter(
            user=request.user,
            year=date.today().year
        ).select_related("leave_type")

        return render(request, self.template_name, {
            "form": form,
            "leave_balances": leave_balances,
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
    template_name = "faculty/home.html"

from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from adminapp.models import LeaveApplication


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