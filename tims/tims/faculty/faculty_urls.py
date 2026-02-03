from django.urls import path
from .views import ApplyLeaveView, MyLeavesView, DeleteLeaveView

urlpatterns = [
    path("leave/apply/", ApplyLeaveView.as_view(), name="faculty_apply_leave"),
    path("leave/my/", MyLeavesView.as_view(), name="faculty_my_leaves"),
    path("leave/delete/<int:leave_id>/", DeleteLeaveView.as_view(), name="faculty_delete_leave"),
]
