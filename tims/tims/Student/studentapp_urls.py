from django.urls import path
from .views import *
app_name = "Student"

urlpatterns=[
    path("student_register/", StudentRegisterView.as_view(), name="student_register"),

]