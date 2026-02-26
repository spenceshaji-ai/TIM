from django.urls import path

from .views import Home3View

app_name = "Admin" 
urlpatterns = [
    path("admin3", Home3View.as_view(), name="home3"),
]