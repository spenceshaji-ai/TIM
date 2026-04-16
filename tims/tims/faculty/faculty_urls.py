from django.urls import path
from django.views.generic import TemplateView
from .views import ApplyLeaveView, FacultyDashboardView, FacultyMaterialAddView, LeaveCalendarDataView, MyLeavesView, DeleteLeaveView




from tims.faculty.views import (
    TrainingSessionCreateView,
    TrainingSessionListView,
    TrainingSessionUpdateView,
    TrainingSessionDeleteView,
    Home1View,
    FacultyReportCreateView,
    FacultyReportListView,
    FacultyReportUpdateView,
    FacultyReportDeleteView,
    FacultyStudentListView,
    FacultyTrainingProgressView,
    FacultyBatchCompletionRequestCreateView,
    FacultyBatchCompletionRequestListView,
    FacultyBatchCompletionRequestDeleteView,
    StudentAttendanceCreateView,

)


app_name = "faculty"
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

    path('', Home1View.as_view(), name='home1'),
     path("sessions/", TrainingSessionListView.as_view(), name="training_list"),
    path("sessions/create/", TrainingSessionCreateView.as_view(), name="training_create"),
    path("sessions/<int:pk>/update/", TrainingSessionUpdateView.as_view(), name="training_update"),
    path("sessions/<int:pk>/delete/", TrainingSessionDeleteView.as_view(), name="training_delete"),

    path("attendance/create/", StudentAttendanceCreateView.as_view(), name="attendance-create"),
   
    path('reports/', FacultyReportListView.as_view(), name='faculty_report_list'),
    path('reports/add/', FacultyReportCreateView.as_view(), name='faculty_report_create'),
    path('reports/edit/<int:pk>/', FacultyReportUpdateView.as_view(), name='faculty_report_update'),
    path('reports/delete/<int:pk>/', FacultyReportDeleteView.as_view(), name='faculty_report_delete'),

    path("students/",FacultyStudentListView.as_view(),name="faculty_student_list"),  
    path("completion-request/create/", FacultyBatchCompletionRequestCreateView.as_view(), name="completion-request-create"),
    path("completion-requests/", FacultyBatchCompletionRequestListView.as_view(), name="completion-request-list"),
    path("completion-request/delete/<int:pk>/", FacultyBatchCompletionRequestDeleteView.as_view(), name="completion-request-delete"),
    
    path("students/",FacultyStudentListView.as_view(),name="faculty_student_list"),  
    path("leave/apply/", ApplyLeaveView.as_view(), name="faculty_apply_leave"),
    path("leave/my/", MyLeavesView.as_view(), name="faculty_my_leaves"),
    path("leave/delete/<int:leave_id>/", DeleteLeaveView.as_view(), name="faculty_delete_leave"),
     path(
        "materials/add/",
        FacultyMaterialAddView.as_view(),
        name="material_add"
    ),
    path('', Home1View.as_view(), name='home2')
    
]


