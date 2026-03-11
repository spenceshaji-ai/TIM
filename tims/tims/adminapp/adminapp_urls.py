from django.urls import path
from django.views.generic import TemplateView
from .views import *

from .views import AdmissionListView
from .views import StaffListCreateView, FacultyListCreateView,EditStaffView


app_name = "adminapp"

urlpatterns = [

    # Dashboard

    # ================= SALARY =================
# ===============================
    # 1️⃣ SALARY STRUCTURE
    # ===============================
    path("salary/structure/",
         SalaryStructureListView.as_view(),
         name="salary_structure_list"),

    path("salary/set/<int:user_id>/",
         SalaryStructureCreateUpdateView.as_view(),
         name="salary_set"),

    path("salary/preview/<int:pk>/",
         SalaryPreviewView.as_view(),
         name="salary_preview"),   

    # ===============================
    # 2️⃣ MONTHLY SALARY GENERATION
    # ===============================
    path(
        "salary/monthly/",
        MonthlySalaryUserListView.as_view(),
        name="monthly_salary_users"
    ),

        path(
    "salary/generate/<int:user_id>/",
    MonthlySalaryGenerateView.as_view(),
    name="generate_salary"
),

    path(
        "salary/history/<int:user_id>/",
        SalaryHistoryView.as_view(),
        name="salary_history"
    ),

    # ===============================
    # 4️⃣ ALL GENERATED SALARIES
    # ===============================
    path(
        "salary/list/",
        SalaryListView.as_view(),
        name="salary_list"
    ),



    # ================= HOLIDAY =================
    path("holiday/add/", HolidayCreateView.as_view(), name="holiday_add"),
    path("holidays/", HolidayListView.as_view(), name="holiday_list"),
    path("holidays/edit/<int:pk>/", HolidayUpdateView.as_view(), name="holiday_edit"),
    path("holidays/delete/<int:pk>/", HolidayDeleteView.as_view(), name="holiday_delete"),
    # ================= LEAVE MAIN =================
    path("leave/requests/", LeaveRequestsView.as_view(), name="leave_requests"),

    path(
        "leave-update/<int:leave_id>/<str:status>/",
        UpdateLeaveStatusView.as_view(),
        name="update_leave_status",
    ),

    # 🔥 USERS LIST PAGE (Search + Assign + View)
    path("leave-users/", LeaveUserListView.as_view(), name="leave_users"),

    # 🔥 USER LEAVE HISTORY PAGE
    path(
        "leave-history/<int:user_id>/",
        LeaveHistoryDetailView.as_view(),
        name="leave_history_detail"
    ),

    # 🔥 HR ASSIGN LEAVE PAGE
    path(
        "hr/assign-leave/<int:user_id>/",
        HRLeaveAssignView.as_view(),
        name="hr_leave_assign",
    ),

    # 🔥 CALENDAR
    path("leave-calendar/data/", LeaveCalendarDataView.as_view(), name="leave_calendar_data"),
    path(
        "leave-calendar/",
        TemplateView.as_view(template_name="adminapp/leave_calendar.html"),
        name="leave_calendar"
    ),

    # 🔥 MONTHLY + YEARLY ACTIONS (NO HTML NEEDED)
    path("leave/monthly-accrual/", MonthlyAccrualView.as_view(), name="monthly_accrual"),
    path("leave/yearly-reset/", YearlyResetView.as_view(), name="yearly_reset"),

    # ================= MANAGEMENT =================
    path(
        "management/apply-leave/",
        ManagementApplyLeaveView.as_view(),
        name="management_apply_leave"
    ),

    path(
        "management/my-leaves/",
        ManagementMyLeavesView.as_view(),
        name="management_my_leaves"
    ),

    path(
        "management/delete-leave/<int:leave_id>/",
        ManagementDeleteLeaveView.as_view(),
        name="management_delete_leave"
    ),

    # ================= COURSES =================
    path("",Home2View.as_view(),name='home2'),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/add/", CourseCreateView.as_view(), name="course_add"),
    path("courses/edit/<int:id>/", CourseEditView.as_view(), name="course_edit"),
    path("courses/delete/<int:id>/", CourseDeleteView.as_view(), name="course_delete"),

    # ================= BATCH =================
    path("batches/", BatchListView.as_view(), name="batch_list"),
    path("batches/add/", BatchCreateView.as_view(), name="batch_add"),
    path("batches/edit/<int:id>/", BatchEditView.as_view(), name="batch_edit"),
    path("batches/delete/<int:id>/", BatchDeleteView.as_view(), name="batch_delete"),

    # ================= FACULTY =================
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
    path("faculty-assignments/view/", FacultyCoursesView.as_view(), name="faculty_courses"),

    # ================= STUDENTS =================
    path("assign-students/add/", AssignStudentView.as_view(), name="assign_student"),
    path("assignments/", AssignStudentListView.as_view(), name="assign_student_list"),
    path("assignments/edit/<int:pk>/", AssignStudentEditView.as_view(), name="assign_student_edit"),
    path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(), name="assign_student_delete"),

    path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(),
         name="assign-student-delete"),

     

 
  
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
    path("followups/", FollowUpListView.as_view(), name="followup_list"),
    path("enquiry/<int:enquiry_id>/followup/add/",FollowUpCreateView.as_view(),name="followup_add"),
    path("admissions/", AdmissionListView.as_view(), name="admission_list"),
    path("enquiry/<int:enquiry_id>/convert/",ConvertToAdmissionView.as_view(),name="convert_admission"),
    
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

   

    path("faculty-assignments/add/", FacultyAssignmentCreateView.as_view(), name="faculty_assignment"),
    path("faculty-assignments/view/",FacultyCoursesView.as_view(),name="faculty_courses"),

    path('admin/training-approvals/', TrainingSessionApprovalListView.as_view(), name='admin_training_approval_list'),
    path('admin/training-approve/<int:pk>/', TrainingSessionApproveView.as_view(), name='training_approve'),
    path('admin/training-reject/<int:pk>/', TrainingSessionRejectView.as_view(), name='training_reject'),
   #path(
       # "faculty-assignments/<int:pk>/delete/",
        #views.faculty_assignment_delete,
        #name="faculty_assignment_delete",
    #)
    path("assign-students/add/", AssignStudentView.as_view(), name="assign-student"),
    path("assignments/", AssignStudentListView.as_view(),name="assign-student-list"),
    path("assignments/edit/<int:pk>/", AssignStudentEditView.as_view(),name="assign-student-edit"),
    path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(),name="assign-student-delete"),
    path("faculty-reports/",AdminFacultyReportListView.as_view(),name="faculty_report_list",),
    path("training-sessions/",AdminTrainingSessionListView.as_view(),name="training_session_list",),
    path("assignment-report/", AssignmentReportView.as_view(), name="assignment-report"),


# from tims.adminapp.views import LeaveHistoryDetailView, LeaveRequestsView, LeaveUserListView, UpdateLeaveStatusView, LeaveRequestsView,UpdateLeaveStatusView,FollowUpCreateView, FollowUpListView
# from .views import *
# from .views import (
#     EnquiryListView,
#     EnquiryCreateView,
#     EnquiryDetailView,
#     EnquiryUpdateView,
#     EnquiryDeleteView,
# )

# from .views import ConvertToAdmissionView, AdmissionListView
# from .views import (
#     TrainingSessionApprovalListView,
#     TrainingSessionApproveView,
#     TrainingSessionRejectView,
#     AdminFacultyReportListView,
#     AdminTrainingSessionListView
# )



       path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(),
         name="assign-student-delete"),
       path("cert_add/", CertificateCreateView.as_view(), name="add"),
       # path("list/", CertificateListView.as_view(), name="list"),    
       path('mark-completed/', MarkCompletedStudentsView.as_view(), name='mark-completed'),
       path("certificate/add/<int:student_id>/", CertificateCreateView.as_view(), name="add_certificate_for_student"), 
       path('feedbacks/', AdminFeedbackListView.as_view(), name='admin_feedback_list'),
       path('', Home2View.as_view(), name='home2'),

]
