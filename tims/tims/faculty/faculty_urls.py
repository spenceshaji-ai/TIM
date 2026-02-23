from django.urls import path
from .views import *

app_name = "faculty"


urlpatterns = [
    path(
        "materials/add/",
        FacultyMaterialAddView.as_view(),
        name="material_add"
    ),
    path('', Home1View.as_view(), name='home1')
]

