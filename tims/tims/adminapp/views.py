# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from adminapp.models import Course,Batch,FacultyAssignment,Assignstudent
from tims.faculty.models import TrainingSession,FacultyDailyReport,StudentAttendance
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CourseForm,BatchForm,FacultyAssignmentForm,AssignstudentForm
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_time, parse_datetime

# List
class CourseListView(View):
    template_name="course_list.html"

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
        return redirect("adminapp:batch_list")
    

class FacultyAssignmentCreateView(View):
    template_name = "faculty_assignment.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": FacultyAssignmentForm()
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
