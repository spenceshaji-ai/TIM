from django.urls import path
from django.views.generic import TemplateView
from .views import ApplyLeaveView, FacultyDashboardView, LeaveCalendarDataView, MyLeavesView, DeleteLeaveView
app_name = "faculty"
from django.urls import path
from .views import ApplyLeaveView, MyLeavesView



urlpatterns = [
  
    path("", FacultyDashboardView.as_view(), name="dashboard"),
path(
        "apply-leave/",
        ApplyLeaveView.as_view(),
        name="faculty_apply_leave"
    ),

    path(
        "my-leaves/",
        MyLeavesView.as_view(),
        name="faculty_my_leaves"
    ),

    path(
        "delete-leave/<int:leave_id>/",
        DeleteLeaveView.as_view(),
        name="delete_leave"
    ),
    path(
        "leave-calendar/",
        TemplateView.as_view(
            template_name="faculty/leave_calendar.html"
        ),
        name="leave_calendar"
    ),
    path(
        "leave-calendar/data/",
        LeaveCalendarDataView.as_view(),
        name="leave_calendar_data"
    ),

]
