from django.urls import path
from .views import ApplyLeaveView, FacultyDashboardView, MyLeavesView, DeleteLeaveView

urlpatterns = [
    path("", FacultyDashboardView.as_view(), name="dashboard"),
    path("leave/apply/", ApplyLeaveView.as_view(), name="faculty_apply_leave"),
    path("leave/my/", MyLeavesView.as_view(), name="faculty_my_leaves"),
    path("leave/delete/<int:leave_id>/", DeleteLeaveView.as_view(), name="faculty_delete_leave"),
]
