# from django.views import View
# from django.shortcuts import render, redirect, get_object_or_404
# from Student.models import JobApplication,Student
# from .forms import StudentForm,ApplicationForm
# from Admin.models import Job,Jobtype
# from django.views.generic import ListView
# from django.contrib.auth import get_user_model
# User = get_user_model()



# class StudentRegisterView(View):

#     def get(self, request):
#         form = StudentForm()
#         return render(request, "student/student_register.html", {"form": form})

#     def post(self, request):
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             student = form.save()   
#             return redirect('student_register') 

#         return render(request, "student/student_register.html", {"form": form})
    

# #Student job application


# class StudentApplyJobView(View):
#     template_name = "student/studentapplyjob.html"

#     def get(self, request, job_id):
#         job = get_object_or_404(Job, id=job_id)

#         # Pre-fill job field
#         form = ApplicationForm(initial={"job": job})
#         return render(request, self.template_name, {
#             "form": form,
#             "job": job
#         })

#     def post(self, request, job_id):
#         job = get_object_or_404(Job, id=job_id)
#         form = ApplicationForm(request.POST, request.FILES)

#         if form.is_valid():
#             student_name = "Rahul Menon"

#             try:
#                 student = Student.objects.get(name=student_name)
#             except Student.DoesNotExist:
#                 return redirect("job_list")

#             application = form.save(commit=False)
#             application.student = student
#             application.job = job
#             application.status = "Applied"
#             application.save()

#             # After success → back to job list
#             return redirect("job_list")

#         return render(request, self.template_name, {
#             "form": form,
#             "job": job
#         })





#     ###NEW 
# class StudentJobListView(ListView):
#     model = Job
#     template_name = "student/Studentjoblist.html"
#     context_object_name = "jobs"

#     def get_queryset(self):
#         queryset = Job.objects.select_related("job_type")
#         job_type_id = self.request.GET.get("job_type")

#         if job_type_id:
#             queryset = queryset.filter(job_type_id=job_type_id)

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["job_types"] = Jobtype.objects.all()
#         context["selected_job_type"] = self.request.GET.get("job_type")
#         return context   
    

# from django.http import JsonResponse
# from django.views import View

# class StudentJobDetailView(View):
#     def get(self, request, pk):
#         job = Job.objects.get(pk=pk)
#         data = {
#             "id": job.id,
#             "title": job.title,
#             "company": job.company,
#             "location": job.location,
#             "salary": job.salary,
#             "job_type": job.job_type.job_type,
#         }
#         return JsonResponse(data)


    
# class StudentApplicationTrackingView(View):
#     template_name = "student/studentapplicationtracking.html"

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         name = request.POST.get("name")
#         applications = None
#         if name:
#             applications = JobApplication.objects.filter(
#                 student__name__icontains=name
#             ).select_related("job", "student").order_by("-applied_date")
#         return render(request, self.template_name, {
#             "applications": applications,
#             "searched_name": name
#         })


from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.http import JsonResponse
from tims.Student.models import JobApplication, Student
from tims.Admin.models import Job, Jobtype
from .forms import StudentForm, ApplicationForm
from django.utils import timezone

User = get_user_model()



# Student Registration

from django.shortcuts import render, redirect
from django.views import View
from tims.Student.models import Student
from .forms import StudentForm
from django.contrib.auth import get_user_model
User = get_user_model()
from tims.adminapp.models import Batch,FacultyAssignment,Assignstudent,Batch
from tims.faculty.models import TrainingSession,FacultyDailyReport,StudentAttendance
from django.contrib.auth.mixins import LoginRequiredMixin
class StudentRegisterView(View):
    template_name="student_register.html"
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
# from Student.models import Student
# from .forms import StudentForm

# class StudentRegisterView(View):
#     template_name="student_register.html"

#     def get(self, request):
#         form = StudentForm()
#         return render(
#             request,
#             self.template_name,
#             {"form": form}
#         )

#     def post(self, request):
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # ✅ redirect back to registration page
#             return redirect("Student:student_register")

#         # ❌ if form is invalid, show same page with errors
#         return render(
#             request,
#             self.template_name,
#             {"form": form}
#         )
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from tims.faculty.models import FacultyCourseMaterial
from tims.adminapp.models import Assignstudent

class stdHome(View):
    def get(self, request):
        return render(request, "stdhome.html")
    

# users/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from tims.adminapp.models import Certificate

class MyIssuedCertificatesView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request):
        certificates = Certificate.objects.filter(student__student=request.user)
        return render(request, 'my_certificates.html', {'certificates': certificates})


# Detail view: Preview a single certificate
class CertificateDetailView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, pk):
        certificate = get_object_or_404(
            Certificate, pk=pk, student__student=request.user
        )
        return render(request, 'certificate_prev.html', {'certificate': certificate})

class StudentCourseMaterialsView(View):
    template_name = "student_course_materials.html"

    def get(self, request):

        # 1️⃣ Authentication check
        if not request.user.is_authenticated:
            return render(request, "access_denied.html")

        # 2️⃣ Role check (make sure case matches DB exactly)
        if not request.user.role or request.user.role.role_name.lower() != "student":
            return render(request, "access_denied.html")

        # 3️⃣ Get assignments for this user
        assignments = Assignstudent.objects.filter(
            student_id=request.user.id   # safer than student=request.user
        )

        # 4️⃣ If no assignment → no materials
        if not assignments.exists():
            return render(request, self.template_name, {
                "materials": []
            })

        # 5️⃣ Get batch IDs
        batch_ids = assignments.values_list("batch_id", flat=True)

        # 6️⃣ Get materials based on batch
        materials = FacultyCourseMaterial.objects.filter(
            batch_id__in=batch_ids
        ).order_by("-created_at")

        return render(request, self.template_name, {
            "materials": materials
        })

from .forms import FeedbackForm

class FeedbackCreateView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, certificate_id):
        # Only allow students to give feedback for their own certificates
        certificate = get_object_or_404(Certificate, id=certificate_id, student__student=request.user)

        # Check if feedback already exists
        # if hasattr(certificate, 'feedback'):
        #     return render(request, "feedback_already_submitted.html", {"certificate": certificate})

        form = FeedbackForm()
        return render(request, "feedback_form.html", {"form": form, "certificate": certificate})

    def post(self, request, certificate_id):
        certificate = get_object_or_404(Certificate, id=certificate_id, student__student=request.user)

        if hasattr(certificate, 'feedback'):
            return render(request, "feedback_already_submitted.html", {"certificate": certificate})

        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.certificate = certificate
            feedback.save()
            return render(request, "feedback_success.html", {"certificate": certificate})

        return render(request, "feedback_form.html", {"form": form, "certificate": certificate})

# ===============================
# Apply Job
# ===============================

class StudentApplyJobView(LoginRequiredMixin, View):

    template_name = "student/studentapplyjob.html"

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)

        # deadline check
        if job.application_deadline < timezone.now().date():
            return redirect("job_list")

        # duplicate check
        if JobApplication.objects.filter(job=job, student=request.user).exists():
            return redirect("job_list")

        form = ApplicationForm()

        return render(request, self.template_name, {"form": form, "job": job})

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)

        if job.application_deadline < timezone.now().date():
            return redirect("job_list")

        if JobApplication.objects.filter(job=job, student=request.user).exists():
            return redirect("job_list")

        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.job = job
            application.status = "Applied"
            application.save()
            return redirect("job_list")

        return render(request, self.template_name, {"form": form, "job": job})


# ===============================
# Job List
# ===============================

class StudentJobListView(LoginRequiredMixin, ListView):

    model = Job
    template_name = "student/Studentjoblist.html"
    context_object_name = "jobs"

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()
        applied_jobs = JobApplication.objects.filter(student=user).values_list("job_id", flat=True)
        status = self.request.GET.get("status", "active")
        queryset = Job.objects.select_related("job_type")

        # 🔥 FILTER LOGIC
        if status == "active":
            queryset = queryset.filter(application_deadline__gte=today).exclude(id__in=applied_jobs)
        elif status == "applied":
            queryset = queryset.filter(id__in=applied_jobs)
        elif status == "expired":
            queryset = queryset.filter(application_deadline__lt=today)

        # Job type filter
        job_type_id = self.request.GET.get("job_type")
        if job_type_id:
            queryset = queryset.filter(job_type_id=job_type_id)

        return queryset.order_by("-posted_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_types"] = Jobtype.objects.all()
        context["selected_job_type"] = self.request.GET.get("job_type")
        context["today"] = timezone.now().date()
        context["selected_status"] = self.request.GET.get("status", "active")
        context["applied_jobs"] = list(
            JobApplication.objects.filter(student=self.request.user).values_list("job_id", flat=True)
        )
        return context


# ===============================
# Job Detail (AJAX)
# ===============================

class StudentJobDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        is_expired = job.application_deadline < timezone.now().date()
        is_applied = JobApplication.objects.filter(job=job, student=request.user).exists()

        data = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "salary": job.salary,
            "job_type": job.job_type.job_type,
            "application_deadline": job.application_deadline.strftime("%Y-%m-%d"),
            "is_expired": is_expired,
            "is_applied": is_applied,
            "description": getattr(job, "description", "No description available"),
            "qualification": getattr(job, "qualification", "Not specified"),
            "skills": getattr(job, "skills", "Not specified"),
        }

        return JsonResponse(data)



# Student Application Tracking


# class StudentApplicationTrackingView(View):
#     template_name = "student/studentapplicationtracking.html"

#     def get(self, request):

#         # 1. Check login
#         if not request.user.is_authenticated:
#             return redirect("login")

#         # 2. Get student using logged-in email
#         try:
#             student = Student.objects.get(email=request.user.email)
#         except Student.DoesNotExist:
#             # If student profile not created
#             return redirect("student_register")

#         # 3. Get only this student's applications
#         applications = JobApplication.objects.filter(
#             student=student
#         ).select_related("job").order_by("-applied_date")

#         # 4. Send to template
#         return render(request, self.template_name, {
#             "applications": applications
#         })

# ===============================
# Application Tracking
# ===============================

class StudentApplicationTrackingView(LoginRequiredMixin, View):

    template_name = "student/studentapplicationtracking.html"

    def get(self, request):

        status_filter = request.GET.get("status")

        applications = JobApplication.objects.filter(
            student=request.user
        ).select_related(
            "job",
            "interview"
        )

        if status_filter:
            applications = applications.filter(
                status=status_filter
            )

        applications = applications.order_by(
            "-applied_date"
        )

        return render(request, self.template_name, {
            "applications": applications,
            "selected_status": status_filter
        })



       

class StudentProgressView(LoginRequiredMixin, View):
    template_name = "progress.html"

    def get(self, request):

        student = request.user   # 🔐 only logged student

        # Get assigned batch
        assignment = Assignstudent.objects.filter(
            student=student
        ).select_related('batch', 'batch__course').first()

        batch = assignment.batch if assignment else None

        # Attendance calculation
        total_classes = StudentAttendance.objects.filter(
            student=student
        ).count()

        present_classes = StudentAttendance.objects.filter(
            student=student,
            status="Present"
        ).count()

        attendance_percentage = 0
        if total_classes > 0:
            attendance_percentage = round(
                (present_classes / total_classes) * 100, 2
            )

        context = {
            "student": student,
            "batch": batch,
            "course": batch.course if batch else None,
            "attendance_percentage": attendance_percentage,
            "total_classes": total_classes,
            "present_classes": present_classes,
        }

        return render(request, self.template_name, context)

class StudentTrainingSessionView(LoginRequiredMixin, View):
    template_name = "training_sessions.html"

    def get(self, request):

        # Assigned batch & course for this student
        student_assignments = Assignstudent.objects.filter(
            student=request.user
        ).select_related("batch", "course")

        batch_ids = student_assignments.values_list("batch_id", flat=True)

        # Date filter
        session_date = request.GET.get("session_date")

        sessions = TrainingSession.objects.filter(
            batch_id__in=batch_ids
        ).select_related("batch", "faculty").order_by("-session_date")

        if session_date:
            sessions = sessions.filter(session_date=session_date)

        context = {
            "sessions": sessions,
            "student_assignments": student_assignments,
            "selected_date": session_date,
        }

        return render(request, self.template_name, context) 


class HomeView1(View):
    def get(self, request):
        user = request.user

        # Job stats
        total_applications = JobApplication.objects.filter(student=user).count()
        applied_jobs = JobApplication.objects.filter(student=user, status="Applied").count()

        # Attendance
        total_classes = StudentAttendance.objects.filter(student=user).count()
        present_classes = StudentAttendance.objects.filter(student=user, status="Present").count()

        attendance_percentage = 0
        if total_classes > 0:
            attendance_percentage = round((present_classes / total_classes) * 100, 2)

        # Training sessions
        batch_ids = Assignstudent.objects.filter(student=user).values_list("batch_id", flat=True)

        sessions = TrainingSession.objects.filter(
            batch_id__in=batch_ids,
            approval_status="Approved"
        ).count()

        context = {
            "user": user,
            "total_applications": total_applications,
            "applied_jobs": applied_jobs,
            "attendance_percentage": attendance_percentage,
            "total_classes": total_classes,
            "present_classes": present_classes,
            "sessions": sessions,
        }

        return render(request, "stdhome.html", context)      
           
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.views import View
from tims.adminapp.models import Certificate


class CertificateDownloadView(View):

    def get(self, request, pk):
        certificate = get_object_or_404(
            Certificate,
            pk=pk,
            student__student=request.user
        )

        response = render(request, "certificate_prev.html", {
            "certificate": certificate
        })

        response["Content-Disposition"] = (
            f'attachment; filename="Certificate_{certificate.certificate_number}.html"'
        )

        return response

from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from tims.Student.models import Feedback


class CourseRatingsView(View):

    template_name = "course_ratings.html"

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect("users:login")

        # Aggregate ratings course-wise
        course_ratings_qs = (
            Feedback.objects
            .values(
                "certificate__student__course__id",
                "certificate__student__course__course_name"
            )
            .annotate(
                avg_rating=Avg("rating"),
                total_reviews=Count("id")
            )
            .order_by("-avg_rating")
        )

        course_ratings = []

        for course in course_ratings_qs:
            course_id = course["certificate__student__course__id"]

            # Fetch related reviews for this course
            reviews = Feedback.objects.filter(
                certificate__student__course__id=course_id
            ).select_related(
                "certificate__student__student"
            ).order_by("-submitted_on")

            course_ratings.append({
                "course_name": course["certificate__student__course__course_name"],
                "avg_rating": course["avg_rating"],
                "total_reviews": course["total_reviews"],
                "reviews": reviews
            })

        context = {
            "course_ratings": course_ratings
        }

        return render(request, self.template_name, context)