from django.urls import path
from .views import *



from .views import (
    #RegisterView,
    LoginView,
    LogoutView,
    role_based_redirect,
    staff_dashboard,
    student_dashboard,
    UserRegisterView,
    RoleCreateView
)


app_name = "users"
urlpatterns = [
    #path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("redirect/", role_based_redirect, name="role_redirect"),
    path("staff/dashboard/", staff_dashboard, name="staff_dashboard"),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),


    #path("~redirect/", view=user_redirect_view, name="redirect"),
    #path("~update/", view=user_update_view, name="update"),
    #path("<str:username>/", view=user_detail_view, name="detail"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("role/add/", RoleCreateView.as_view(), name="role_add"),
]


