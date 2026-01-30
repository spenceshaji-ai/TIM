from django.urls import path
from .views import (
    ApplyLeaveView,
    MyLeavesView,
    DeleteLeaveView,
    LeaveRequestsView,
    UpdateLeaveStatusView,
)

urlpatterns = [
    path("leave/apply/", ApplyLeaveView.as_view(), name="apply_leave"),
    path("leave/my/", MyLeavesView.as_view(), name="my_leaves"),
    path("leave/delete/<int:leave_id>/", DeleteLeaveView.as_view(), name="delete_leave"),
    path("leave/requests/", LeaveRequestsView.as_view(), name="leave_requests"),
    path(
        "leave/<int:leave_id>/<str:status>/",
        UpdateLeaveStatusView.as_view(),
        name="update_leave_status",
    ),
]
