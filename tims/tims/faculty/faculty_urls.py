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


app_name = "faculty"
urlpatterns = [

    path('training-sessions/', TrainingSessionList.as_view(), name='training_list'),
    path('training-sessions/create/', TrainingSessionCreate.as_view(), name='training_create'),
    path('training-sessions/<int:pk>/update/', TrainingSessionUpdate.as_view(), name='training_update'),
    path('training-sessions/<int:pk>/delete/', TrainingSessionDelete.as_view(), name='training_delete'),
    path('add/', AttendanceCreate.as_view(), name='attendance_add'),
    path('list/', AttendanceList.as_view(), name='attendance_list'),
    path('update/<int:pk>/', AttendanceUpdate.as_view(), name='attendance_update'),
    path('delete/<int:pk>/', AttendanceDelete.as_view(), name='attendance_delete'),
]
