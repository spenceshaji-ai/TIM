from django.views.generic import CreateView, ListView, View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.utils.timezone import now
from adminapp.models import LeaveApplication, LeaveBalance, LeaveType
from .forms import LeaveApplicationForm



class FacultyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "faculty/home.html"


from datetime import date

from datetime import date
from django.utils.timezone import now
from django.contrib import messages
from adminapp.models import LeaveApplication, LeaveBalance, LeaveType


class ApplyLeaveView(LoginRequiredMixin, View):
    template_name = "faculty/apply_leave.html"

    def get(self, request):

        current_year = date.today().year

        leave_balances = LeaveBalance.objects.filter(
            user=request.user,
            year=current_year
        ).select_related("leave_type")

        leave_types = LeaveType.objects.all()

        return render(request, self.template_name, {
            "leave_balances": leave_balances,
            "leave_types": leave_types,
            "today": now().date(),
        })

    def post(self, request):

        leave_type_id = request.POST.get("leave_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        day_type = request.POST.get("day_type")

        leave_type = LeaveType.objects.get(id=leave_type_id)

        leave = LeaveApplication(
            user=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            day_type=day_type,
            status="Pending"
        )

        try:
            leave.full_clean()
            leave.save()
            messages.success(request, "Leave request submitted successfully.")
            return redirect("faculty:faculty_my_leaves")

        except Exception as e:
            messages.error(request, str(e))

        # Reload balances on error
        leave_balances = LeaveBalance.objects.filter(
            user=request.user,
            year=date.today().year
        ).select_related("leave_type")

        leave_types = LeaveType.objects.all()

        return render(request, self.template_name, {
            "leave_balances": leave_balances,
            "leave_types": leave_types,
            "today": now().date(),
        })
from django.utils.timezone import now

class MyLeavesView(LoginRequiredMixin, ListView):
    model = LeaveApplication
    template_name = "faculty/my_leaves.html"
    context_object_name = "leaves"

    def get_queryset(self):
        self.request.session["leave_last_seen"] = now().isoformat()

        return LeaveApplication.objects.filter(
            user=self.request.user
        ).select_related("leave_type").order_by("-applied_at")



class DeleteLeaveView(LoginRequiredMixin, View):

    def get(self, request, leave_id):
        LeaveApplication.objects.filter(
            id=leave_id,
            user=request.user,
            status="Pending"
        ).delete()

        messages.info(request, "Pending leave deleted.")
        return redirect("faculty:faculty_my_leaves")
    
    # adminapp/views.py  (or leaves/views.py – wherever you keep leave logic)

import calendar
from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from adminapp.models import LeaveApplication
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



