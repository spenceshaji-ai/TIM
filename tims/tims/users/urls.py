from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view,role_redirect_view,StaffDashboardView,StudentDashboardView
from .views import user_update_view
from .views import (
    UserListView,
    UserCreateView,
    UserEditView,
    UserDeleteView
)
from .views import (
    EnquiryListView,
    EnquiryCreateView,
    EnquiryDetailView,
    EnquiryUpdateView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("redirect/", role_redirect_view, name="role_redirect"),
    path("staff-dashboard/",StaffDashboardView.as_view(),name="staff_dashboard"),
    path( "student-dashboard/",StudentDashboardView.as_view(),name="student_dashboard",
),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    path("users/", UserListView.as_view(), name="user_list"),
    path("users/add/", UserCreateView.as_view(), name="user_add"),
    path("users/edit/<int:pk>/", UserEditView.as_view(), name="user_edit"),
    path("users/delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("enquiry/", EnquiryListView.as_view(), name="enquiry_list"),
    path("enquiry/add/", EnquiryCreateView.as_view(), name="enquiry_add"),
    path("enquiry/<int:pk>/", EnquiryDetailView.as_view(), name="enquiry_detail"),
    path("enquiry/<int:pk>/edit/", EnquiryUpdateView.as_view(), name="enquiry_edit"),

]
