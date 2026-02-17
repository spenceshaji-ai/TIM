# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from tims.adminapp.models import Course, Batch, Enquiry, FollowUp, Admission,Payment
from .forms import CourseForm, BatchForm, EnquiryForm, FollowUpForm, AdmissionForm,PaymentForm


from tims.adminapp.models import FacultyAssignment,Assignstudent
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import FacultyAssignmentForm,AssignstudentForm
from django.contrib import messages
from django.db import models
from django.db.models import Sum



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
            return redirect("adminapp:enquiry_list")

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
    
class MarkNotInterestedView(View):

    def get(self, request, enquiry_id):
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        enquiry.status = "Not Interested"
        enquiry.save()

        return redirect("adminapp:enquiry_detail", pk=enquiry.id)

    
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

            return redirect("adminapp:" \
            "enquiry_detail", pk=enquiry.id)

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
            "course": enquiry.course,
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

            return redirect("adminapp:admission_list")

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })
    
class AdmissionListView(View):
    template_name = "admission/admission_list.html"

    def get(self, request):
        admissions = Admission.objects.all().order_by("-admission_date")
        for adm in admissions:
            paid = adm.payments.aggregate(
                total=models.Sum("amount")
              )["total"] or 0

            adm.paid_amount = paid
            adm.pending_amount = adm.course.fee - paid

        return render(request, self.template_name, {
             "admissions": admissions
         })


    



# -----------------------------
# Payment Create View
# -----------------------------


class PaymentCreateView(View):

    def post(self, request):
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)

            admission = payment.admission
            total_fee = admission.course.fee

            paid_total = admission.payments.aggregate(
                total=Sum("amount")
            )["total"] or 0

            new_amount = payment.amount

            # 🚨 VALIDATION
            if paid_total >= total_fee:
                form.add_error(None, "Fees already fully paid.")
                return render(request, "payment/payment_form.html", {"form": form})

            if paid_total + new_amount > total_fee:
                remaining = total_fee - paid_total
                form.add_error(
                    "amount",
                    f"Amount exceeds pending fee. Remaining: {remaining}"
                )
                return render(request, "payment/payment_form.html", {"form": form})

            payment.save()
            return redirect("adminapp:payment_list")

        return render(request, "payment/payment_form.html", {"form": form})



# -----------------------------
# Payment List View
# -----------------------------
class PaymentListView(View):

    def get(self, request):
        payments = Payment.objects.select_related("admission").all()
        # 🔥 Add calculations for each payment row
        for p in payments:

            total_fee = p.admission.course.fee   # Total course fee

            paid = p.admission.payments.aggregate(
                total=Sum("amount")
            )["total"] or 0   # Total paid so far

            p.total_fee = total_fee
            p.paid_amount = paid
            p.pending_fee = total_fee - paid

        return render(
            request,
            "payment/payment_list.html",
            {"payments": payments}
        )

class PaymentUpdateView(View):
    template_name = "payment/payment_form.html"

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        form = PaymentForm(instance=payment)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        form = PaymentForm(request.POST, instance=payment)

        if form.is_valid():
            form.save()
            return redirect("adminapp:payment_list")

        return render(request, self.template_name, {"form": form})


class PaymentDeleteView(View):

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return redirect("adminapp:payment_list")

    

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
