# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Course,Batch
from .forms import CourseForm,BatchForm
from .models import Enquiry, FollowUp
from .forms import EnquiryForm,FollowUpForm
from .models import Admission
from .forms import AdmissionForm
from adminapp.models import Course,Batch,FacultyAssignment,Assignstudent
from tims.faculty.models import TrainingSession,FacultyDailyReport,StudentAttendance
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CourseForm,BatchForm,FacultyAssignmentForm,AssignstudentForm
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_time, parse_datetime

# List
class CourseListView(View):
    template_name = "course_list.html"

    def get(self, request):
        courses = Course.objects.all()
        return render(request, self.template_name, {"courses": courses})

# ADD
class CourseCreateView(View):
    template_name = "course_add.html"

    def get(self, request):
        form = CourseForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:course_list')
        return render(request, self.template_name, {"form": form})

# EDIT
class CourseEditView(View):
    template_name = "course_edit.html"

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        form = CourseForm(instance=course)
        return render(request, self.template_name, {
            "form": form,
            "course": course
        })

    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('adminapp:course_list')
        return render(request, self.template_name, {
            "form": form,
            "course": course
        })

# DELETE (separate page)
class CourseDeleteView(View):

    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        course.delete()
        return redirect('adminapp:course_list')


class BatchCreateView(View):
    template_name="batch_add.html"

    def get(self, request):
        form = BatchForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminapp:batch_list")
        return render(request, self.template_name, {"form": form})

class BatchListView(View):
    template_name="batch_list.html"

    def get(self, request):
        batches = Batch.objects.select_related("course")
        return render(request, self.template_name, {"batches": batches})


class BatchEditView(View):
    template_name = "batch_add.html"

    def get(self, request, id):
        batch = get_object_or_404(Batch, id=id)
        form = BatchForm(instance=batch)
        return render(request, self.template_name, {
            "form": form,
            "batch": batch
        })

    def post(self, request, id):
        batch = get_object_or_404(Batch, id=id)
        form = BatchForm(request.POST, instance=batch)

        if form.is_valid():
            form.save()
            return redirect("adminapp:batch_list")

        return render(request, self.template_name, {
            "form": form,
            "batch": batch
        })

class BatchDeleteView(View):
    def post(self, request, id):
        batch = get_object_or_404(Batch, id=id)
        batch.delete()
        return redirect("batch_list")
    
class EnquiryListView(View):
    template_name = "enquiry/enquiry_list.html"

    def get(self, request):
        enquiries = Enquiry.objects.all().order_by("-created_at")
        return render(request, self.template_name, {"enquiries": enquiries})

class EnquiryCreateView(View):
    template_name = "enquiry/enquiry_form.html"

    def get(self, request):
        form = EnquiryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EnquiryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("enquiry_list")

        return render(request, self.template_name, {"form": form})

class EnquiryDetailView(View):
    template_name = "enquiry/enquiry_detail.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        return render(request, self.template_name, {"enquiry": enquiry})

class EnquiryUpdateView(View):
    template_name = "enquiry/enquiry_form.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        form = EnquiryForm(instance=enquiry)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        form = EnquiryForm(request.POST, instance=enquiry)

        if form.is_valid():
            form.save()
            return redirect("enquiry_list")

        return render(request, self.template_name, {"form": form})

class EnquiryDeleteView(View):
    template_name = "enquiry/enquiry_delete.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        return render(request, self.template_name, {"enquiry": enquiry})

    def post(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        enquiry.delete()
        return redirect("enquiry_list")
    
#FOLLOWUP
class FollowUpCreateView(View):
    template_name = "followup/followup_form.html"

    def get(self, request, enquiry_id):
        form = FollowUpForm()
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })

    def post(self, request, enquiry_id):
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        form = FollowUpForm(request.POST)

        if form.is_valid():
            followup = form.save(commit=False)
            followup.enquiry = enquiry
            followup.save()

            return redirect("enquiry_detail", pk=enquiry.id)

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })
    
class FollowUpListView(View):
    template_name = "followup/followup_list.html"

    def get(self, request):
        followups = FollowUp.objects.all().order_by("-followup_date")
        return render(request, self.template_name, {"followups": followups})


class ConvertToAdmissionView(View):
    template_name = "admission/admission_form.html"

    def get(self, request, enquiry_id):

        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        # ✅ Pre-fill data from Enquiry
        form = AdmissionForm(initial={
            "student_name": enquiry.name,
            "phone": enquiry.phone,
            "email": enquiry.email,
            "course": enquiry.course_id,
        })

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })

    def post(self, request, enquiry_id):

        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        form = AdmissionForm(request.POST)

        if form.is_valid():
            admission = form.save(commit=False)
            admission.enquiry = enquiry
            admission.save()

            # ✅ Update Enquiry Status
            enquiry.status = "Converted"
            enquiry.save()

            return redirect("admission_list")

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })
    
class AdmissionListView(View):
    template_name = "admission/admission_list.html"

    def get(self, request):
        admissions = Admission.objects.all().order_by("-admission_date")
        return render(request, self.template_name, {
            "admissions": admissions
        })

        return redirect("adminapp:batch_list")
    

class FacultyAssignmentCreateView(View):
    template_name = "faculty_assignment.html"

class FacultyAssignmentCreateView(View):
    def get(self, request):
        form = FacultyAssignmentForm()
        return render(request, "adminapp/faculty_assignment.html", {
            "form": form
        })

    def post(self, request):
        form = FacultyAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty assigned successfully")
            return redirect("adminapp:faculty_courses")

        return render(request, self.template_name, {"form": form})

class FacultyCoursesView(View):
    template_name = "facultylist.html"

    def get(self, request):
        faculty_id = request.GET.get("faculty")

        # Only users with Faculty role
        faculties = User.objects.filter(role__role_name="Faculty")

        assignments = None
        if faculty_id:
            assignments = (
                FacultyAssignment.objects
                .filter(faculty_id=faculty_id)
                .select_related("course", "batch")
            )

        return render(request, self.template_name, {
            "faculties": faculties,
            "assignments": assignments,
        })
from django.views.generic import CreateView, ListView, View
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
from adminapp.models import LeaveApplication


class LeaveRequestsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LeaveApplication
    template_name = "adminapp/leave_requests.html"
    context_object_name = "leaves"

    def test_func(self):
        return self.request.user.is_staff


class UpdateLeaveStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, leave_id, status):
        leave = get_object_or_404(LeaveApplication, id=leave_id)
        leave.status = status
        leave.save()
        return redirect("leave_requests")


class LeaveUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "adminapp/leave_users.html"
    context_object_name = "users"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return User.objects.filter(
            leaveapplication__status="Approved"
        ).distinct()


class LeaveHistoryDetailView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LeaveApplication
    template_name = "adminapp/leave_history.html"
    context_object_name = "leaves"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return LeaveApplication.objects.filter(
            user_id=self.kwargs["user_id"],
            status="Approved"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faculty"] = User.objects.get(id=self.kwargs["user_id"])
        return context


class TrainingSessionApprovalListView(View):
    template_name = "training_approval_list.html"

    def get(self, request):
        sessions = TrainingSession.objects.all().order_by('-created_at')
        return render(request, self.template_name, {
            'sessions': sessions
        })

class TrainingSessionApproveView(View):
    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        session.approval_status = 'Approved'
        session.save()
        return redirect('adminapp:admin_training_approval_list')

class TrainingSessionRejectView(View):
    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        session.approval_status = 'Rejected'
        session.save()
        return redirect('adminapp:admin_training_approval_list')


class AssignStudentView(View):
    template_name = "student_assignment.html"

    def get(self, request):
        form = AssignstudentForm()
        assignments = Assignstudent.objects.all()
        return render(request, self.template_name, {
            "form": form,
            "assignments": assignments
        })

    def post(self, request):
        form = AssignstudentForm(request.POST)
        assignments = Assignstudent.objects.all()

        if form.is_valid():
            form.save()
            return redirect("adminapp:assign-student-list")

        return render(request, self.template_name, {
            "form": form,
            "assignments": assignments
        })

class AssignStudentListView(View):
    template_name = "assign_studentlist.html"

    def get(self, request):
        assignments = Assignstudent.objects.select_related(
            "student", "course", "batch"
        )
        return render(request, self.template_name, {
            "assignments": assignments
        })
    
class AssignStudentEditView(View):
    template_name = "student_assignment.html"

    def get(self, request, pk):
        assignment = get_object_or_404(Assignstudent, pk=pk)
        form = AssignstudentForm(instance=assignment)
        return render(request, self.template_name, {
            "form": form,
            "assignment": assignment
        })

    def post(self, request, pk):
        assignment = get_object_or_404(Assignstudent, pk=pk)
        form = AssignstudentForm(request.POST, instance=assignment)

        if form.is_valid():
            form.save()
            return redirect("adminapp:assign-student-list")

        return render(request, self.template_name, {
            "form": form,
            "assignment": assignment
        })

class AssignStudentDeleteView(View):
    def get(self, request, pk):
        assignment = get_object_or_404(Assignstudent, pk=pk)
        assignment.delete()
        return redirect("adminapp:assign-student-list")


class AdminFacultyReportListView(View):
    template_name = "faculty_report_list.html"

    def get(self, request):

        reports = FacultyDailyReport.objects.select_related('faculty')

        # Date filter
        date_filter = request.GET.get('date')

        if date_filter:
            parsed_date = parse_date(date_filter)
            if parsed_date:
                reports = reports.filter(report_date=parsed_date)

        context = {
            "reports": reports,
            "selected_date": date_filter,
        }

        return render(request, self.template_name, context)

class AdminTrainingSessionListView(View):
    template_name = "training_session_list.html"

    def get(self, request):

        sessions = TrainingSession.objects.select_related(
            "faculty", "batch"
        ).all()

        # Filters
        batch_id = request.GET.get("batch")
        faculty_id = request.GET.get("faculty")
        status = request.GET.get("status")

        if batch_id:
            sessions = sessions.filter(batch_id=batch_id)

        if faculty_id:
            sessions = sessions.filter(faculty_id=faculty_id)

        if status:
            sessions = sessions.filter(status=status)

        # Get all batches
        batches = Batch.objects.all()

        # Get only faculty users (role = Faculty)
        faculties = User.objects.filter(role__role_name="Faculty")

        context = {
            "sessions": sessions,
            "batches": batches,
            "faculties": faculties,
            "selected_batch": batch_id,
            "selected_faculty": faculty_id,
            "selected_status": status,
        }

        return render(request, self.template_name, context)

class AssignmentReportView(View):
    template_name = "assignment_report.html"

    def get(self, request):

        course_id = request.GET.get("course")
        batch_id = request.GET.get("batch")
        role_filter = request.GET.get("role")

        users = []

        # ================= STUDENT FILTER =================
        if role_filter == "student":
            assigned_students = Assignstudent.objects.select_related(
                "student", "batch", "batch__course"
            )

            if course_id:
                assigned_students = assigned_students.filter(
                    batch__course_id=course_id
                )

            if batch_id:
                assigned_students = assigned_students.filter(
                    batch_id=batch_id
                )

            for assign in assigned_students:
                user = assign.student

                total = StudentAttendance.objects.filter(
                    student=user
                ).count()

                present = StudentAttendance.objects.filter(
                    student=user,
                    status="Present"
                ).count()

                attendance_percentage = 0
                if total > 0:
                    attendance_percentage = round((present / total) * 100, 2)

                users.append({
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone_number,
                    "attendance": attendance_percentage,
                })

        # ================= FACULTY FILTER =================
        elif role_filter == "faculty":
            assigned_faculty = FacultyAssignment.objects.select_related(
                "faculty", "batch", "batch__course"
            )

            if course_id:
                assigned_faculty = assigned_faculty.filter(
                    batch__course_id=course_id
                )

            if batch_id:
                assigned_faculty = assigned_faculty.filter(
                    batch_id=batch_id
                )

            for assign in assigned_faculty:
                user = assign.faculty

                users.append({
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone_number,
                    "attendance": None,
                })

        context = {
            "courses": Course.objects.all(),
            "batches": Batch.objects.all(),
            "report_data": users,
            "selected_course": course_id,
            "selected_batch": batch_id,
            "selected_role": role_filter,
        }

        return render(request, self.template_name, context)
