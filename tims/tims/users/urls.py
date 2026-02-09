from django.urls import path

"""(from .views import user_detail_view
from .views import user_redirect_view,role_redirect_view,StaffDashboardView,StudentDashboardView
from .views import user_update_view
from .views import (
    UserListView,
    UserCreateView,
    UserEditView,
    UserDeleteView
))"""

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    role_based_redirect,
    staff_dashboard,
    student_dashboard,
)


app_name = "users"
"""(urlpatterns = [
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
   

])"""

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("redirect/", role_based_redirect, name="role_redirect"),
    path("staff/dashboard/", staff_dashboard, name="staff_dashboard"),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
]
