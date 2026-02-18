from django.urls import path
from .views import *
from adminapp.views import (
    TrainingSessionApprovalListView,
    TrainingSessionApproveView,
    TrainingSessionRejectView,
    AdminFacultyReportListView,
    AdminTrainingSessionListView
)

app_name = "adminapp"

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/add/", CourseCreateView.as_view(), name="course_add"),
    path("courses/edit/<int:id>/", CourseEditView.as_view(), name="course_edit"),
    path("courses/delete/<int:id>/", CourseDeleteView.as_view(), name="course_delete"),

    path("batches/", BatchListView.as_view(), name="batch_list"),
    path("batches/add/", BatchCreateView.as_view(), name="batch_add"),
    path("batches/edit/<int:id>/", BatchEditView.as_view(), name="batch_edit"),
    path("batches/delete/<int:id>/", BatchDeleteView.as_view(), name="batch_delete"),

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
  