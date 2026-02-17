from django.urls import path
from .views import UserListView




# from .views import (
#     #RegisterView,
#     LoginView,
#     LogoutView,
#     role_based_redirect,
#     staff_dashboard,
#     student_dashboard,
#     UserRegisterView,
#     RoleCreateView
# )

from .views import (
    LoginView,
    LogoutView,
    RoleBasedRedirectView,
    StaffDashboardView,
    StudentDashboardView,
    UserRegisterView,
    RoleCreateView
)



app_name = "users"
urlpatterns = [
    #path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("redirect/", RoleBasedRedirectView.as_view(), name="role_redirect"),
    path("staff/dashboard/", StaffDashboardView.as_view(), name="staff_dashboard"),
    path("student/dashboard/", StudentDashboardView.as_view(), name="student_dashboard"),



    #path("~redirect/", view=user_redirect_view, name="redirect"),
    #path("~update/", view=user_update_view, name="update"),
    #path("<str:username>/", view=user_detail_view, name="detail"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("role/add/", RoleCreateView.as_view(), name="role_add"),


    path("user-list/", UserListView.as_view(), name="user_list"),


]


