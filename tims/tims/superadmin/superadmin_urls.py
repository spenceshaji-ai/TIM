from django.urls import path

from .views import *

app_name="superadmin"

urlpatterns = [
    path("", Home5View.as_view(), name="home5"),
]