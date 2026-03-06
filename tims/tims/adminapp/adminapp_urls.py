from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = "adminapp"

urlpatterns = [

    # Dashboard
    path("", AdminDashboardView.as_view(), name="home"),

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
    path("management/leave/apply/", ManagementLeaveApplyView.as_view(), name="management_leave_apply"),
    path("management/leave/list/", ManagementLeaveListView.as_view(), name="management_leave_list"),

    # ================= COURSES =================
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
    path("faculty-assignments/add/", FacultyAssignmentCreateView.as_view(), name="faculty_assignment"),
    path("faculty-assignments/view/", FacultyCoursesView.as_view(), name="faculty_courses"),

    # ================= STUDENTS =================
    path("assign-students/add/", AssignStudentView.as_view(), name="assign_student"),
    path("assignments/", AssignStudentListView.as_view(), name="assign_student_list"),
    path("assignments/edit/<int:pk>/", AssignStudentEditView.as_view(), name="assign_student_edit"),
    path("assignments/delete/<int:pk>/", AssignStudentDeleteView.as_view(), name="assign_student_delete"),
]