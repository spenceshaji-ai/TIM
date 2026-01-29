from django.urls import path
from .views import (
    TrainingSessionCreate,
    TrainingSessionUpdate,
    TrainingSessionList,
    TrainingSessionDelete,
    AttendanceCreate,
    AttendanceList,
    AttendanceUpdate,
    AttendanceDelete
)


from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    path('training-sessions/', TrainingSessionList.as_view(), name='training_list'),
    path('training-sessions/create/', TrainingSessionCreate.as_view(), name='training_create'),
    path('training-sessions/<int:pk>/update/', TrainingSessionUpdate.as_view(), name='training_update'),
    path('training-sessions/<int:pk>/delete/', TrainingSessionDelete.as_view(), name='training_delete'),
    path('add/', AttendanceCreate.as_view(), name='attendance_add'),
    path('list/', AttendanceList.as_view(), name='attendance_list'),
    path('update/<int:pk>/', AttendanceUpdate.as_view(), name='attendance_update'),
    path('delete/<int:pk>/', AttendanceDelete.as_view(), name='attendance_delete'),
]


