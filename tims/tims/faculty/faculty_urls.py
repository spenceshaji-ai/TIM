from django.urls import path
from tims.faculty.views import ApplyLeaveView, MyLeavesView, DeleteLeaveView


from tims.faculty.views import (
    TrainingSessionCreateView,
    TrainingSessionListView,
    TrainingSessionUpdateView,
    TrainingSessionDeleteView,
    StudentAttendanceListView,
    StudentAttendanceCreate,
    StudentAttendanceUpdateView,
    StudentAttendanceDeleteView,
    FacultyTrainingProgressView,
    Home1View,
    FacultyReportCreateView,
    FacultyReportListView,
    FacultyReportUpdateView,
    FacultyReportDeleteView,
    FacultyStudentListView,
    FacultyTrainingProgressView
)


app_name = "faculty"
urlpatterns = [
    path('', Home1View.as_view(), name='home1'),
    path("sessions/", TrainingSessionListView.as_view(), name="training_list"),
    path("sessions/create/", TrainingSessionCreateView.as_view(), name="training_create"),
    path("sessions/<int:pk>/update/", TrainingSessionUpdateView.as_view(), name="training_update"),
    path("sessions/<int:pk>/delete/", TrainingSessionDeleteView.as_view(), name="training_delete"),

    path('list', StudentAttendanceListView.as_view(), name='attendance-list'),
    path('create/', StudentAttendanceCreate.as_view(), name='attendance-create'),
    path('update/<int:pk>/', StudentAttendanceUpdateView.as_view(), name='attendance-update'),
    path('delete/<int:pk>/', StudentAttendanceDeleteView.as_view(), name='attendance-delete'),
    
    path("training-progress/", FacultyTrainingProgressView.as_view(), name="faculty_training_progress"),

    path('reports/', FacultyReportListView.as_view(), name='faculty_report_list'),
    path('reports/add/', FacultyReportCreateView.as_view(), name='faculty_report_create'),
    path('reports/edit/<int:pk>/', FacultyReportUpdateView.as_view(), name='faculty_report_update'),
    path('reports/delete/<int:pk>/', FacultyReportDeleteView.as_view(), name='faculty_report_delete'),

    path("students/",FacultyStudentListView.as_view(),name="faculty_student_list"),  
    path("leave/apply/", ApplyLeaveView.as_view(), name="faculty_apply_leave"),
    path("leave/my/", MyLeavesView.as_view(), name="faculty_my_leaves"),
    path("leave/delete/<int:leave_id>/", DeleteLeaveView.as_view(), name="faculty_delete_leave"),
    
]
