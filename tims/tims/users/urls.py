from django.urls import path
from .views import (
    LoginView,
    LogoutView,   
    UserRegisterView,
    RoleCreateView,
    UserListView
)



app_name = "users"
urlpatterns = [
    
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),   
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("role/add/", RoleCreateView.as_view(), name="role_add"),
    path("user-list/", UserListView.as_view(), name="user_list"),
    path("logout/", LogoutView.as_view(), name="logout"),



]


