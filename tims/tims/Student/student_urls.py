from django.urls import path
from .views import (
    StudentRegisterView,
    JobApplicationCreateView,
    JobApplicationListView,
    JobApplicationEditView,
   
)

urlpatterns = [
    # Student
    path('students/register/', StudentRegisterView.as_view(), name='student_register'),

    # Job Applications
    path('applications/', JobApplicationListView.as_view(), name='application_list'),
    path('applications/create/', JobApplicationCreateView.as_view(), name='application_create'),
    path('applications/edit/<int:id>/', JobApplicationEditView.as_view(), name='application_edit'),
]
