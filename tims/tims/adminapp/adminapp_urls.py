from django.urls import path
from . import views
from .views import *
from .views import (
    EnquiryListView,
    EnquiryCreateView,
    EnquiryDetailView,
    EnquiryUpdateView,
    EnquiryDeleteView,
)
from .views import FollowUpCreateView, FollowUpListView
from .views import ConvertToAdmissionView, AdmissionListView

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
    path("enquiries/", EnquiryListView.as_view(), name="enquiry_list"),
    path("enquiries/add/", EnquiryCreateView.as_view(), name="enquiry_add"),
    path("enquiries/<int:pk>/", EnquiryDetailView.as_view(), name="enquiry_detail"),
    path("enquiries/<int:pk>/edit/", EnquiryUpdateView.as_view(), name="enquiry_edit"),
    path("enquiries/<int:pk>/delete/", EnquiryDeleteView.as_view(), name="enquiry_delete"),
    path("followups/", FollowUpListView.as_view(), name="followup_list"),
    path("enquiry/<int:enquiry_id>/followup/add/",FollowUpCreateView.as_view(),name="followup_add"),
    path("admissions/", AdmissionListView.as_view(), name="admission_list"),
    path("enquiry/<int:enquiry_id>/convert/",ConvertToAdmissionView.as_view(),name="convert_admission"),

]   

