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
from adminapp.models import Assignstudent

class stdHome(View):
    def get(self, request):
        return render(request, "stdhome.html")
    

# users/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from adminapp.models import Certificate

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

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.views import View
from adminapp.models import Certificate


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
        