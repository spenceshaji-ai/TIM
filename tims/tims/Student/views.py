

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
from Student.models import JobApplication, Student
from Admin.models import Job, Jobtype
from .forms import StudentForm, ApplicationForm
from django.utils import timezone

User = get_user_model()



# Student Registration

class StudentRegisterView(View):
    template_name = "student/student_register.html"

    def get(self, request):
        form = StudentForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('student_register')

        return render(request, self.template_name, {"form": form})



# Student Job Application

class StudentApplyJobView(View):
    template_name = "student/studentapplyjob.html"

    # -------- GET METHOD --------
    def get(self, request, job_id):

        # 1. Check if user is logged in
        if not request.user.is_authenticated:
            return redirect("login")

        # 2. Get the selected job
        job = get_object_or_404(Job, id=job_id)

        # 🚨 Deadline check
        if job.application_deadline < timezone.now().date():
            return redirect("job_list")

        # 3. Find Student profile using logged-in user's email
        try:
            student = Student.objects.get(email=request.user.email)
        except Student.DoesNotExist:
            return redirect("student_register")

        # 🚨 Duplicate application check
        already_applied = JobApplication.objects.filter(
            job=job,
            student=student
        ).exists()

        if already_applied:
            return redirect("job_list")

        # 4. Create empty form
        form = ApplicationForm()

        # 5. Send form and job to template
        return render(request, self.template_name, {
            "form": form,
            "job": job
        })

    # -------- POST METHOD --------
    def post(self, request, job_id):

        # 1. Check login
        if not request.user.is_authenticated:
            return redirect("login")

        # 2. Get job
        job = get_object_or_404(Job, id=job_id)

        # 🚨 Deadline check
        if job.application_deadline < timezone.now().date():
            return redirect("job_list")

        # 3. Get student profile
        try:
            student = Student.objects.get(email=request.user.email)
        except Student.DoesNotExist:
            return redirect("student_register")

        # 🚨 Duplicate check
        if JobApplication.objects.filter(job=job, student=student).exists():
            return redirect("job_list")

        # 4. Get form data + resume file
        form = ApplicationForm(request.POST, request.FILES)

        # 5. Validate form
        if form.is_valid():

            application = form.save(commit=False)
            application.student = student
            application.job = job
            application.status = "Applied"
            application.save()

            return redirect("job_list")

        # 6. If form invalid, reload page
        return render(request, self.template_name, {
            "form": form,
            "job": job
        })




# Student Job List

class StudentJobListView(ListView):
    model = Job
    template_name = "student/Studentjoblist.html"
    context_object_name = "jobs"

    def get_queryset(self):
        queryset = Job.objects.select_related("job_type").order_by("-posted_date")
        job_type_id = self.request.GET.get("job_type")
        if job_type_id:
            queryset = queryset.filter(job_type_id=job_type_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_types"] = Jobtype.objects.all()
        context["selected_job_type"] = self.request.GET.get("job_type")
        context["today"] = timezone.now().date()   # <-- ADD THIS
        return context


# Student Job Detail (JSON)

class StudentJobDetailView(View):
    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        is_expired = job.application_deadline < timezone.now().date()

        data = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "salary": job.salary,
            "job_type": job.job_type.job_type,
            "application_deadline": job.application_deadline.strftime("%Y-%m-%d"),
            "is_expired": is_expired,
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


class StudentApplicationTrackingView(View):
    template_name = "student/studentapplicationtracking.html"

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect("login")

        try:
            student = Student.objects.get(email=request.user.email)
        except Student.DoesNotExist:
            return redirect("student_register")

        # Get filter value from URL
        status_filter = request.GET.get("status")

        applications = JobApplication.objects.filter(
            student=student
        ).select_related(
            "job",
            "interview"
        )

        # Apply status filter
        if status_filter:
            applications = applications.filter(status=status_filter)

        applications = applications.order_by("-applied_date")

        return render(request, self.template_name, {
            "applications": applications,
            "selected_status": status_filter
        })

class HomeView1(View):
    def get(self, request):
        return render(request, "student/home.html")