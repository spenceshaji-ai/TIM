from django.urls import path
from .views import (
    StudentRegisterView,
    StudentJobListView,
    StudentJobDetailView,
    StudentApplyJobView,
    StudentApplicationTrackingView,
    HomeView1,
)
urlpatterns = [
    # Student
    path('students/register/', StudentRegisterView.as_view(), name='student_register'),
    
    #Student Apply for Job
    path("student/apply/<int:job_id>/", StudentApplyJobView.as_view(), name="student_apply_job"),

  
    path("studentjobs/", StudentJobListView.as_view(), name="job_list"),


    path("studentjobs/<int:pk>/", StudentJobDetailView.as_view(), name="student_job_detail"),

    path('studentjobtrack/', StudentApplicationTrackingView.as_view(), name='track_applications'),

    path('std/', HomeView1.as_view(), name='studenthome'),




]
