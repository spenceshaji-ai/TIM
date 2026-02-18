from django.urls import path
from .views import LeaveHistoryDetailView, LeaveRequestsView, LeaveUserListView, UpdateLeaveStatusView
from .views import *
from .views import (
    EnquiryListView,
    EnquiryCreateView,
    EnquiryDetailView,
    EnquiryUpdateView,
    EnquiryDeleteView,
)
from .views import FollowUpCreateView, FollowUpListView
from .views import ConvertToAdmissionView, AdmissionListView
from adminapp.views import (
    TrainingSessionApprovalListView,
    TrainingSessionApproveView,
    TrainingSessionRejectView,
    AdminFacultyReportListView,
    AdminTrainingSessionListView
)

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
    path("enquiries/", EnquiryListView.as_view(), name="enquiry_list"),
    path("enquiries/add/", EnquiryCreateView.as_view(), name="enquiry_add"),
    path("enquiries/<int:pk>/", EnquiryDetailView.as_view(), name="enquiry_detail"),
    path("enquiries/<int:pk>/edit/", EnquiryUpdateView.as_view(), name="enquiry_edit"),
    path("enquiries/<int:pk>/delete/", EnquiryDeleteView.as_view(), name="enquiry_delete"),
    path("followups/", FollowUpListView.as_view(), name="followup_list"),
    path("enquiry/<int:enquiry_id>/followup/add/",FollowUpCreateView.as_view(),name="followup_add"),
    path("admissions/", AdmissionListView.as_view(), name="admission_list"),
    path("enquiry/<int:enquiry_id>/convert/",ConvertToAdmissionView.as_view(),name="convert_admission"),

    path("leave/apply/", ApplyLeaveView.as_view(), name="apply_leave"),
    path("leave/my/", MyLeavesView.as_view(), name="my_leaves"),
    path("leave/delete/<int:leave_id>/", DeleteLeaveView.as_view(), name="delete_leave"),



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
   

    path("faculty-assignments/add/", FacultyAssignmentCreateView.as_view(), name="faculty_assignment"),
    path("faculty-assignments/view/",FacultyCoursesView.as_view(),name="faculty_courses"),

    path('admin/training-approvals/', TrainingSessionApprovalListView.as_view(), name='admin_training_approval_list'),
    path('admin/training-approve/<int:pk>/', TrainingSessionApproveView.as_view(), name='training_approve'),
    path('admin/training-reject/<int:pk>/', TrainingSessionRejectView.as_view(), name='training_reject'),
    
    

   #path(
       # "faculty-assignments/<int:pk>/delete/",
        #views.faculty_assignment_delete,
        #name="faculty_assignment_delete",
    #)
 
    path("assign-students/add/", AssignStudentView.as_view(), name="assign-student"),
    path("assignments/", AssignStudentListView.as_view(),name="assign-student-list"),
    path("assignments/edit/<int:pk>/", AssignStudentEditView.as_view(),name="assign-student-edit"),
    path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(),name="assign-student-delete"),

    path("faculty-reports/",AdminFacultyReportListView.as_view(),name="faculty_report_list",),
    path("training-sessions/",AdminTrainingSessionListView.as_view(),name="training_session_list",),
    path("assignment-report/", AssignmentReportView.as_view(), name="assignment-report")

] 
  
