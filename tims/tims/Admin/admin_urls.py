

from django.urls import path
from .views import (
    JobCreateView,
    JobListView,
    JobEditView,
    JobDeleteView,
    JobtypeCreateView,
    JobtypeListView,
    JobtypeEditView,
    JobtypeDeleteView,
    
    AdminApplicationListView,
    AdminApplicationShortlistView,
    AdminApplicationRejectView,
    ScheduleInterviewView,
    AdminApplicationSelectView,
    

)
app_name = 'admin_app' 


urlpatterns = [
    path('jobtype/create/', JobtypeCreateView.as_view(), name='jobtype_create'),
    path('jobtype/', JobtypeListView.as_view(), name='jobtype_list'),
    path('jobtype/<int:pk>/edit/', JobtypeEditView.as_view(), name='jobtype_edit'),
    path('jobtype/<int:pk>/delete/', JobtypeDeleteView.as_view(), name='jobtype_delete'),



    path('jobview/', JobListView.as_view(), name='job_list'),
    path('companyjobcreate/', JobCreateView.as_view(), name='job_create'),
    path('edit/<int:id>/', JobEditView.as_view(), name='job_edit'),
    path('delete/<int:id>/', JobDeleteView.as_view(), name='job_delete'),

    

   
    

   

    path('applications/', AdminApplicationListView.as_view(), name='admin_application_list'),
    path('applications/<int:id>/shortlist/', AdminApplicationShortlistView.as_view(), name='admin_application_approve'),
    path('applications/<int:id>/reject/', AdminApplicationRejectView.as_view(), name='admin_application_reject'),

    path('applications/<int:application_id>/schedule-interview/', ScheduleInterviewView.as_view(), name='schedule_interview'),
    path( 'applications/<int:id>/select/', AdminApplicationSelectView.as_view(),name='admin_application_select'),


    

]

  

# from . import views  # make sure this exists at top

# urlpatterns += [
#    path('applicationtracking/',views.JobApplicationTracking,name='applicationtracking_list' ),
#     path('applicationtrackingstatus/<int:pk>/status/<str:status>/',views.JobApplicationTrackingstatus,name='applicationtracking_update'),
# ]