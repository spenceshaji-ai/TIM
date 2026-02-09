from django.views.generic import CreateView, ListView, View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.timezone import now
from adminapp.models import LeaveApplication, LeaveType
from .forms import LeaveApplicationForm


class FacultyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "faculty/home.html"

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
    template_name = "faculty/apply_leave.html"
    success_url = reverse_lazy("faculty_my_leaves")

    def get(self, request, *args, **kwargs):
        ensure_leave_types()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


from django.utils.timezone import now

class MyLeavesView(LoginRequiredMixin, ListView):
    model = LeaveApplication
    template_name = "faculty/my_leaves.html"
    context_object_name = "leaves"

    def get_queryset(self):
        # clear notification
        self.request.session["leave_last_seen"] = now().isoformat()
        return LeaveApplication.objects.filter(user=self.request.user)



class DeleteLeaveView(LoginRequiredMixin, View):
    def get(self, request, leave_id):
        LeaveApplication.objects.filter(
            id=leave_id,
            user=request.user,
            status="Pending"
        ).delete()
        return redirect("faculty_my_leaves")
