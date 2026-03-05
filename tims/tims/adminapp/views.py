# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.timezone import now
from django.db.models import OuterRef, Subquery
import secrets

from tims.adminapp.models import Course, Batch, Enquiry, FollowUp, Admission,Payment
from .forms import CourseForm, BatchForm, EnquiryForm, FollowUpForm, AdmissionForm,PaymentForm
from datetime import date

from tims.adminapp.models import FacultyAssignment,Assignstudent
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import FacultyAssignmentForm,AssignstudentForm
from django.contrib import messages
from django.db import models
from django.db.models import Sum
from tims.users.models import Role,User
from django.contrib import messages



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
        # 🔥 Attach next follow-up date from FollowUp table
        for enquiry in enquiries:
            last_followup = FollowUp.objects.filter(
                enquiry=enquiry
            ).order_by("-id").first()   # latest followup

            
            if last_followup and last_followup.next_followup_date:
                enquiry.next_followup_date = last_followup.next_followup_date
        
        return render(request, self.template_name, {
               "enquiries": enquiries,
               "today": date.today(),   # ⭐ REQUIRED
        })

class EnquiryCreateView(View):
    template_name = "enquiry/enquiry_form.html"

    def get(self, request):
        form = EnquiryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EnquiryForm(request.POST)

        if form.is_valid():
            enquiry=form.save()
             # 🔥 Create FollowUp automatically if date exists
            if enquiry.next_followup_date:
                FollowUp.objects.create(
                    enquiry=enquiry,
                    followup_date=enquiry.next_followup_date,
                    status="Pending"   # or any default
                )
            

            return redirect("adminapp:enquiry_list")

        return render(request, self.template_name, {"form": form})



class EnquiryDetailView(View):
    template_name = "enquiry/enquiry_detail.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)

        followups = FollowUp.objects.filter(
            enquiry=enquiry
        ).order_by("-followup_date")   # 🔥 newest date first

        return render(request, self.template_name, {
            "enquiry": enquiry,
            "followups": followups
        })


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
            return redirect("adminapp:enquiry_list")

        return render(request, self.template_name, {"form": form})

class EnquiryDeleteView(View):
    template_name = "enquiry/enquiry_delete.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        return render(request, self.template_name, {"enquiry": enquiry})

    def post(self, request, pk):
        enquiry = get_object_or_404(Enquiry, pk=pk)
        enquiry.delete()
        return redirect("adminapp:enquiry_list")
    
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
        
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        form = FollowUpForm(initial={
            "followup_date": enquiry.next_followup_date
        })
        
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
            followup.created_by = request.user

            followup.save()
            # 👇 Update enquiry's next follow-up date
            enquiry.next_followup_date = followup.next_followup_date
            enquiry.save()

            return redirect("adminapp:""enquiry_detail", pk=enquiry.id)

        return render(request, self.template_name, {
            "form": form,
            "enquiry": enquiry
        })
class FollowUpListView(View):
    template_name = "followup/followup_list.html"

    def get(self, request, enquiry_id):
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        followups = FollowUp.objects.filter(
            enquiry=enquiry
        ).order_by("-followup_date")   # 🔥 Feb 20 first

        return render(request, self.template_name, {
            
            "followups": followups,
            "enquiry": enquiry
        })
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import FollowUp
from .forms import FollowUpForm


class FollowUpUpdateView(View):
    template_name = "followup/followup_form.html"

    def get(self, request, pk):
        followup = get_object_or_404(FollowUp, id=pk)
        form = FollowUpForm(instance=followup)

        return render(request, self.template_name, {
            "form": form,
            "followup": followup,
            "enquiry":followup.enquiry
        })

    def post(self, request, pk):
        followup = get_object_or_404(FollowUp, id=pk)
        form = FollowUpForm(request.POST, instance=followup)

        if form.is_valid():
            form.save()

            # 🔥 Go back to enquiry detail page
            return redirect("adminapp:enquiry_detail", followup.enquiry_id)

        return render(request, self.template_name, {
            "form": form,
            "followup": followup,
            "enquiry":followup.enquiry
        })
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

        # ⭐ ADD THIS HERE
        users_usernames = list(
            User.objects.values_list("username", flat=True)
        )

        return render(request, self.template_name, {
            "admissions": admissions,
            "users_usernames": users_usernames   # ⭐ PASS TO TEMPLATE
        })



class CreateStudentAccountView(View):

    def post(self, request, admission_id):

        # 🔐 Allow only Admin
        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("adminapp:admission_list")

        admission = get_object_or_404(Admission, id=admission_id)
        enquiry = admission.enquiry

        # ⭐ Correct role name
        student_role = Role.objects.get(role_name="Student")

        # ⭐ Check if already registered
        existing_user = User.objects.filter(username=enquiry.phone).first()

        if existing_user:
            messages.info(request, "Student already registered")
            return redirect("adminapp:admission_list")
        
        # ⭐ Generate random password
        temp_password = secrets.token_urlsafe(8)
        
        # ⭐ Create new account
        User.objects.create_user(
            username=enquiry.phone,
            email=enquiry.email or "",
            password=temp_password,
            role=student_role,
            name=enquiry.name,
            phone_number=enquiry.phone,
            must_change_password=True
            
        )

        enquiry.status = "Converted"
        enquiry.save()

         # ⭐ Show password to admin
        messages.success(
            request,
            f"Student registered successfully. Temporary password: {temp_password}"
        )

        return redirect("adminapp:admission_list")
    



# -----------------------------
# Payment Create View
# -----------------------------


class PaymentCreateView(View):


     # 👉 Show form + admission fee data
    def get(self, request):

        form = PaymentForm()

        admissions = Admission.objects.select_related("course").all()

        admission_data = []

        for adm in admissions:
            total_fee = adm.course.fee

            paid_total = adm.payments.aggregate(
                total=Sum("amount")
            )["total"] or 0

            admission_data.append({
                "id": adm.id,
                "fee": float(total_fee),
                "paid": float(paid_total),
            })

        return render(
            request,
            "payment/payment_form.html",
            {
                "form": form,
                "admission_data": admission_data   # ⭐ MUST send this
            }
        )

    

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

class Home2View(View):
    def get(self, request):
        return render(request, "pages/adminhome.html")


from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()





class StaffListCreateView(View):
    template_name = "staff_list.html"

    # ✅ Show page
    def get(self, request):

        if not request.user.is_superuser:
            return redirect("login")

        staff = User.objects.filter(
            role__role_name__in=["Admin", "HR", "Manager"]
        )

        roles = Role.objects.filter(
            role_name__in=["Admin", "HR", "Manager"]
        )

        return render(request, self.template_name, {
            "staff": staff,
            "roles": roles
        })

    # ✅ Handle form submit
    def post(self, request):

        if not request.user.is_superuser:
            return redirect("login")

        role_id = request.POST.get("role")   # 🔥 get role ID
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        status = request.POST.get("status")

        if not all([role_id, name, username, phone, password]):
            messages.error(request, "All required fields must be filled")
            return redirect("adminapp:staff_list")

    # ✅ Get role using ID
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            messages.error(request, "Invalid role selected")
            return redirect("adminapp:staff_list")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("adminapp:staff_list")

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect("adminapp:staff_list")

        user = User.objects.create(
            username=username,
            name=name,
            email=email,
            phone_number=phone,
            role=role,
            status=status,
            is_staff=True,
            must_change_password=True 
    )

        user.set_password(password)
        user.save()

        messages.success(request, f"{role.role_name} created successfully")
        return redirect("adminapp:staff_list") 

class EditStaffView(View):
    template_name = "edit_staff.html"
    def get(self, request, pk):
        staff = get_object_or_404(User, pk=pk)
        roles = Role.objects.all()

        return render(request, self.template_name, {
            "staff": staff,
            "roles": roles
        })

    def post(self, request, pk=None):
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = User()
        user = User.objects.get(pk=pk)
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.status = request.POST.get("status")
        user.save()
        return redirect("adminapp:staff_list")


class DeleteStaffView(View):

    def post(self, request, pk):

        if not request.user.is_superuser:
            return redirect("login")

        staff = get_object_or_404(User, pk=pk)
        staff.delete()

        return redirect("adminapp:staff_list")

class FacultyListCreateView(View):
    template_name = "faculty_list.html"

    # ✅ Show page
    def get(self, request):
        print("Authenticated:", request.user.is_authenticated)
        print("User:", request.user)
        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")

        faculty = User.objects.filter(role__role_name="Faculty")

        return render(request, self.template_name, {
            "faculty": faculty
        })

    # ✅ Handle form submit
    def post(self, request):


        


        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if not all([name, phone, password]):
            messages.error(request, "All required fields must be filled")
            return redirect("adminapp:faculty_list")

        faculty_role = Role.objects.filter(role_name="Faculty").first()
         # ✅ phone duplicate validation
        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already registered")
            return redirect("adminapp:faculty_list")

        if not faculty_role:
            messages.error(request, "Faculty role not found")
            return redirect("adminapp:faculty_list")

        if User.objects.filter(username=phone).exists():
            messages.error(request, "Faculty already exists")
            return redirect("adminapp:faculty_list")

        User.objects.create_user(
            username=username,
            password=password,
            name=name,
            email=email,
            phone_number=phone,
            role=faculty_role,
            status="active"
        )

        messages.success(request, "Faculty created successfully")
        return redirect("adminapp:faculty_list")

class EditFacultyView(View):
    template_name = "edit_faculty.html"

    def get(self, request, pk):

        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")

        faculty = User.objects.get(id=pk)

        return render(request, self.template_name, {
            "faculty": faculty
        })

    def post(self, request, pk):

        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")

        faculty = User.objects.get(id=pk)

        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        status = request.POST.get("status")

        # username validation
        if User.objects.exclude(id=faculty.id).filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("adminapp:edit_faculty", pk=pk)

        # phone validation
        if User.objects.exclude(id=faculty.id).filter(phone_number=phone).exists():
            messages.error(request, "Phone number already registered")
            return redirect("adminapp:edit_faculty", pk=pk)

        faculty.name = name
        faculty.username = username
        faculty.email = email
        faculty.phone_number = phone
        faculty.status = status

        faculty.save()

        messages.success(request, "Faculty updated successfully")

        return redirect("adminapp:faculty_list")
    
class DeleteFacultyView(View):

    def post(self, request, pk):

        if not (request.user.role and request.user.role.role_name == "Admin"):
            return redirect("login")

        faculty = User.objects.get(id=pk)

        faculty.delete()

        messages.success(request, "Faculty deleted successfully")

        return redirect("adminapp:faculty_list")