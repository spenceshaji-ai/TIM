from django.urls import path

from .views import Home1View

app_name = "faculty" 
urlpatterns = [
    path("", Home1View.as_view(), name="home1"),
]