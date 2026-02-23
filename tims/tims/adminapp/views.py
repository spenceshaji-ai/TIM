# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from adminapp.models import Course,Batch,FacultyAssignment,Assignstudent
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CourseForm,BatchForm,FacultyAssignmentForm,AssignstudentForm,CertificateForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

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
    

from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class CertificateCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "add_certificate.html"
    login_url = "users:login"

    # 🔐 Allow only Admin
    def test_func(self):
        return (
            hasattr(self.request.user, "role") and
            self.request.user.role.role_name == "Admin"
        )

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to access this page.")
        return redirect("home")  # 🔁 change this to your dashboard url name

    def get(self, request):
        form = CertificateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save()
            messages.success(
                request,
                f"Certificate {certificate.certificate_number} issued successfully!"
            )
            return render(request, "certificate_preview.html", {"certificate": certificate})

        return render(request, self.template_name, {"form": form})


    
# adminapp/views.py
from django.utils import timezone
from datetime import timedelta

class MarkCompletedStudentsView(View):
    def get(self, request):
        today = timezone.now().date()
        count = 0

        students = Assignstudent.objects.filter(is_completed=False)

        for student in students:
            # calculate end date (example: course.duration in days)
            course_duration_days = getattr(student.course, "duration_in_days", 0)
            course_end_date = student.joined_on + timedelta(days=course_duration_days)

            if today >= course_end_date:
                student.is_completed = True
                student.completed_on = course_end_date
                student.save()
                count += 1

        messages.success(request, f"{count} student(s) marked as completed.")
        return redirect("adminapp:assign-student-list")

# tims/adminapp/views.py or wherever you keep admin views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from tims.Student.models import Feedback


class AdminFeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = "admin_feedback_list.html"
    context_object_name = "feedbacks"
    ordering = ["-submitted_on"]

    def test_func(self):
        # Allow only Admin role
        return self.request.user.role == "Admin"

class Home2View(View):
    def get(self, request):
        return render(request, "pages/adminhome.html")    