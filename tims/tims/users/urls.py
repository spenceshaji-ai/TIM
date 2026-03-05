from django.urls import path
from .views import(
    UserRegisterView,
    RoleCreateView,
    LoginView,
    RoleBasedLoginView,
    UserRedirectView,
    ) 


app_name = "users"
urlpatterns = [
    path("login/", RoleBasedLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("role/add/", RoleCreateView.as_view(), name="role_add"),
    path("redirect/", UserRedirectView.as_view(), name="redirect"),

    # KEEP THIS LAST
    # path("<str:username>/", user_detail_view, name="detail"),
]



