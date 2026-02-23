from django.urls import path
from .views import *
app_name = "adminapp"

urlpatterns = [
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
        path("cert_add/", CertificateCreateView.as_view(), name="add"),
       # path("list/", CertificateListView.as_view(), name="list"),    
       path('mark-completed/', MarkCompletedStudentsView.as_view(), name='mark-completed'),
       path("certificate/add/<int:student_id>/", CertificateCreateView.as_view(), name="add_certificate_for_student"), 
       path('feedbacks/', AdminFeedbackListView.as_view(), name='admin_feedback_list'),
       path('', Home2View.as_view(), name='home2'),

] 
  