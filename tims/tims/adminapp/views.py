from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

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
