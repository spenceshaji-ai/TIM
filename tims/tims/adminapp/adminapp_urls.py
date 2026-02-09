from django.urls import path
from django.views.generic import TemplateView
from .views import LeaveCalendarDataView, LeaveHistoryDetailView, LeaveRequestsView, LeaveUserListView, UpdateLeaveStatusView
   
from .views import *
app_name = "adminapp"

urlpatterns = [
    path("leave/requests/", LeaveRequestsView.as_view(), name="leave_requests"),
    path(
        "leave/<int:leave_id>/<str:status>/",
        UpdateLeaveStatusView.as_view(),
        name="update_leave_status",
    ),
     path("leave-users/", LeaveUserListView.as_view(), name="leave-users"),
    path(
        "leave-history/<int:user_id>/",
        LeaveHistoryDetailView.as_view(),
        name="leave-history-detail"
    ),
    path("leave-calendar/data/", LeaveCalendarDataView.as_view(), name="leave_calendar_data"),
    path("leave-calendar/", TemplateView.as_view(
    template_name="adminapp/leave_calendar.html"
    ), name="leave_calendar"),

     path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/add/", CourseCreateView.as_view(), name="course_add"),
    path("courses/edit/<int:id>/", CourseEditView.as_view(), name="course_edit"),
    path("courses/delete/<int:id>/", CourseDeleteView.as_view(), name="course_delete"),
    path("batches/", BatchListView.as_view(), name="batch_list"),
    path("batches/add/", BatchCreateView.as_view(), name="batch_add"),
    path("batches/edit/<int:id>/", BatchEditView.as_view(), name="batch_edit"),
    path("batches/delete/<int:id>/", BatchDeleteView.as_view(), name="batch_delete"),
    path("faculty-assignments/add/", FacultyAssignmentCreateView.as_view(), name="faculty_assignment"),
    path("faculty-assignments/view/",FacultyCoursesView.as_view(),name="faculty_courses"),
   #path(
       # "faculty-assignments/<int:pk>/delete/",
        #views.faculty_assignment_delete,
        #name="faculty_assignment_delete",
    #)
    path("assign-students/add/", AssignStudentView.as_view(), name="assign-student"),
    path("assignments/", AssignStudentListView.as_view(),
         name="assign-student-list"),
    
    path("assignments/edit/<int:pk>/", AssignStudentEditView.as_view(),
         name="assign-student-edit"),

    path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(),
         name="assign-student-delete"),

]


  
