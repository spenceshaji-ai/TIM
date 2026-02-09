from django.views.generic import ListView, View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import JsonResponse
User = get_user_model()
from adminapp.models import LeaveApplication


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
        leave.save()  # updated_at auto-updates

        return redirect("leave_requests")


class LeaveUserListView(ListView):
    template_name = "adminapp/leave_users.html"
    context_object_name = "users"

    def get_queryset(self):
        return (
            User.objects
            .filter(leaveapplication__status="Approved")
            .distinct()
        )



class LeaveHistoryDetailView(ListView):
    template_name = "adminapp/leave_history_detail.html"
    context_object_name = "leaves"

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return LeaveApplication.objects.filter(
            user_id=user_id,
            status="Approved"
        ).select_related("leave_type")


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

    
