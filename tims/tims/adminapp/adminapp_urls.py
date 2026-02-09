from django.urls import path
from django.views.generic import TemplateView
from .views import LeaveCalendarDataView, LeaveHistoryDetailView, LeaveRequestsView, LeaveUserListView, UpdateLeaveStatusView

urlpatterns = [
    path("leave/requests/", LeaveRequestsView.as_view(), name="leave_requests"),
    path(
        "leave/<int:leave_id>/<str:status>/",
        UpdateLeaveStatusView.as_view(),
        name="update_leave_status",
    ),
     path("leave-users/", LeaveUserListView.as_view(), name="leave-users"),
    path(
        "leave-history/<int:user_id>/",
        LeaveHistoryDetailView.as_view(),
        name="leave-history-detail"
    ),
    path("leave-calendar/data/", LeaveCalendarDataView.as_view(), name="leave_calendar_data"),
    path("leave-calendar/", TemplateView.as_view(
    template_name="adminapp/leave_calendar.html"
    ), name="leave_calendar"),

]
   