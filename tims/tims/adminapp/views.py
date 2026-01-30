from django.views.generic import CreateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

from adminapp.models import LeaveApplication, LeaveType
from .forms import LeaveApplicationForm


def ensure_leave_types():
    leave_data = [
        ("Casual Leave", 12),
        ("Sick Leave", 10),
        ("Paid Leave", 15),
    ]

    for name, days in leave_data:
        LeaveType.objects.get_or_create(
            leave_name=name,
            defaults={"max_days": days},
        )


class ApplyLeaveView(LoginRequiredMixin, CreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = "adminapp/apply_leave.html"
    success_url = reverse_lazy("my_leaves")

    def get(self, request, *args, **kwargs):
        ensure_leave_types()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MyLeavesView(LoginRequiredMixin, ListView):
    model = LeaveApplication
    template_name = "adminapp/my_leaves.html"
    context_object_name = "leaves"

    def get_queryset(self):
        return LeaveApplication.objects.filter(user=self.request.user)


class DeleteLeaveView(LoginRequiredMixin, View):
    def get(self, request, leave_id):
        LeaveApplication.objects.filter(
            id=leave_id, user=request.user, status="Pending"
        ).delete()
        return redirect("my_leaves")


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
