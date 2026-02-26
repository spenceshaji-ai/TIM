from django.urls import path
from django.views.generic import TemplateView
from .views import *

from .views import *
from .views import AdmissionListView


app_name = "adminapp"

urlpatterns = [

    # Dashboard
    path("", AdminDashboardView.as_view(), name="home"),

    # ================= SALARY =================
path("salary-users/", SalaryUsersView.as_view(), name="salary_users"),

path("salary-history/<int:pk>/",
     UserSalaryHistoryView.as_view(),
     name="user_salary_history"),

path("salary-add/<int:pk>/",
     UserSalaryCreateView.as_view(),
     name="user_salary_add"),

path("salary-update/<int:pk>/",
     SalaryUpdateView.as_view(),
     name="salary_update"),

path("salary-delete/<int:pk>/",
     SalaryDeleteView.as_view(),
     name="salary_delete"),

path("salary-paid/<int:pk>/",
     SalaryMarkPaidView.as_view(),
     name="salary_mark_paid"),

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
    path("management/leave/apply/", ManagementLeaveApplyView.as_view(), name="management_leave_apply"),
    path("management/leave/list/", ManagementLeaveListView.as_view(), name="management_leave_list"),

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


  

    path("faculty-assignments/add/", FacultyAssignmentCreateView.as_view(), name="faculty_assignment"),
    path("faculty-assignments/view/", FacultyCoursesView.as_view(), name="faculty_courses"),

    # ================= STUDENTS =================
    path("assign-students/add/", AssignStudentView.as_view(), name="assign_student"),
    path("assignments/", AssignStudentListView.as_view(), name="assign_student_list"),
    path("assignments/edit/<int:pk>/", AssignStudentEditView.as_view(), name="assign_student_edit"),
    path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(), name="assign_student_delete"),

    path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(),
         name="assign-student-delete"),

] 
  
