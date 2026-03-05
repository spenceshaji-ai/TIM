from django.urls import path

from .views import *
from .views import AdmissionListView
from .views import StaffListCreateView, FacultyListCreateView,EditStaffView


app_name = "adminapp"

urlpatterns = [
    path("",Home2View.as_view(),name='home2'),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/add/", CourseCreateView.as_view(), name="course_add"),
    path("courses/edit/<int:id>/", CourseEditView.as_view(), name="course_edit"),
    path("courses/delete/<int:id>/", CourseDeleteView.as_view(), name="course_delete"),
    path("batches/", BatchListView.as_view(), name="batch_list"),
    path("batches/add/", BatchCreateView.as_view(), name="batch_add"),
    path("batches/edit/<int:id>/", BatchEditView.as_view(), name="batch_edit"),
    path("batches/delete/<int:id>/", BatchDeleteView.as_view(), name="batch_delete"),
    path("enquiries/", EnquiryListView.as_view(), name="enquiry_list"),
    path("enquiries/add/", EnquiryCreateView.as_view(), name="enquiry_add"),
    path("enquiries/<int:pk>/", EnquiryDetailView.as_view(), name="enquiry_detail"),
    path("enquiries/<int:pk>/edit/", EnquiryUpdateView.as_view(), name="enquiry_edit"),
    path("enquiries/<int:pk>/delete/", EnquiryDeleteView.as_view(), name="enquiry_delete"),
    path("followups/<int:enquiry_id>/", FollowUpListView.as_view(), name="followup_list"),
    path("enquiry/<int:enquiry_id>/followup/add/",FollowUpCreateView.as_view(),name="followup_add"),
    path("followup/edit/<int:pk>/",FollowUpUpdateView.as_view(),name="followup_edit"),
    path("enquiry/<int:enquiry_id>/not-interested/",MarkNotInterestedView.as_view(),name="not_interested"),

    path("admissions/", AdmissionListView.as_view(), name="admission_list"),
    path("enquiry/<int:enquiry_id>/convert/",ConvertToAdmissionView.as_view(),name="convert_admission"),
    path("enquiry/<int:admission_id>/create-student/",CreateStudentAccountView.as_view(),name="create_student_account"),
    path("payments/add/", PaymentCreateView.as_view(), name="payment_create"),
    path("payments/", PaymentListView.as_view(), name="payment_list"),
    path("payments/edit/<int:pk>/", PaymentUpdateView.as_view(), name="payment_edit"),
    path("payments/delete/<int:pk>/", PaymentDeleteView.as_view(), name="payment_delete"),
    
    path("staff/", StaffListCreateView.as_view(), name="staff_list"),
    path("faculty/", FacultyListCreateView.as_view(), name="faculty_list"),
   
    path("staff/edit/<int:pk>/", EditStaffView.as_view(), name="edit_staff"),
    path("staff/delete/<int:pk>/", DeleteStaffView.as_view(), name="delete_staff"),
    path("faculty/edit/<int:pk>/",EditFacultyView.as_view(),name="edit_faculty"),

    path("faculty/delete/<int:pk>/",DeleteFacultyView.as_view(),name="delete_faculty"),

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
  
