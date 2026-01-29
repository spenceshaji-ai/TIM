from django.urls import path
from .views import (
    JobCreateView,
    JobListView,
    JobEditView,
    JobDeleteView,
)

urlpatterns = [
    path('', JobListView.as_view(), name='job_list'),
    path('create/', JobCreateView.as_view(), name='job_create'),
    path('edit/<int:id>/', JobEditView.as_view(), name='job_edit'),
    path('delete/<int:id>/', JobDeleteView.as_view(), name='job_delete'),
   
]
