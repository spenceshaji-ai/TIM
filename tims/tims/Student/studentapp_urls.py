from django.urls import path
from .views import *
app_name = "Student"

urlpatterns=[
    path("student_register/", StudentRegisterView.as_view(), name="student_register"),
    path("progress/",StudentProgressView.as_view(),name="progress"),
    path('std/', HomeView1.as_view(), name='studenthome'),
    path("student/training-sessions/",StudentTrainingSessionView.as_view(),name="student_training_sessions")
]