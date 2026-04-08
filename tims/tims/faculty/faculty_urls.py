from django.urls import path
from .views import *
    


app_name = "faculty"
urlpatterns = [
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
    
]
