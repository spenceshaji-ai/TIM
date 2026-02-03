from django.urls import path
from .views import LeaveHistoryDetailView, LeaveRequestsView, LeaveUserListView, UpdateLeaveStatusView

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
]
   