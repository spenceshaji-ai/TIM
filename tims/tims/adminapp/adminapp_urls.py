from django.urls import path
from .views import *
app_name = "adminapp"
from .views import (
    ApplyLeaveView,
    MyLeavesView,
    DeleteLeaveView,
    LeaveRequestsView,
    UpdateLeaveStatusView,
)

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/add/", CourseCreateView.as_view(), name="course_add"),
    path("courses/edit/<int:id>/", CourseEditView.as_view(), name="course_edit"),
    path("courses/delete/<int:id>/", CourseDeleteView.as_view(), name="course_delete"),
    path("batches/", BatchListView.as_view(), name="batch_list"),
    path("batches/add/", BatchCreateView.as_view(), name="batch_add"),
    path("batches/edit/<int:id>/", BatchEditView.as_view(), name="batch_edit"),
    path("batches/delete/<int:id>/", BatchDeleteView.as_view(), name="batch_delete"),
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

