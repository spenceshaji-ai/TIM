from django.urls import path
from .views import (
    TrainingSessionCreateView,
    TrainingSessionListView,
    TrainingSessionUpdateView,
    TrainingSessionDeleteView,
    StudentAttendanceList,
    StudentAttendanceCreate,
    StudentAttendanceUpdate,
    StudentAttendanceDelete,
    FacultyAttendanceProgressView,
    FacultyTrainingProgressView

)


app_name = "faculty"
urlpatterns = [
    path("sessions/", TrainingSessionListView.as_view(), name="training_list"),
    path("sessions/create/", TrainingSessionCreateView.as_view(), name="training_create"),
    path("sessions/<int:pk>/update/", TrainingSessionUpdateView.as_view(), name="training_update"),
    path("sessions/<int:pk>/delete/", TrainingSessionDeleteView.as_view(), name="training_delete"),
    path('list', StudentAttendanceList.as_view(), name='attendance-list'),
    path('create/', StudentAttendanceCreate.as_view(), name='attendance-create'),
    path('update/<int:pk>/', StudentAttendanceUpdate.as_view(), name='attendance-update'),
    path('delete/<int:pk>/', StudentAttendanceDelete.as_view(), name='attendance-delete'),
    path("faculty/attendance-progress/",FacultyAttendanceProgressView.as_view(),name="faculty_attendance_progress"),
    path("faculty/training-progress/",FacultyTrainingProgressView.as_view(),name="faculty_training_progress")

    
]
