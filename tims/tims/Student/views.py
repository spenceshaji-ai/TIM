

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from Student.models import JobApplication,Student
from .forms import StudentForm,ApplicationForm
from Admin.models import Job,Jobtype
from django.views.generic import ListView



class StudentRegisterView(View):

    def get(self, request):
        form = StudentForm()
        return render(request, "student/student_register.html", {"form": form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()   
            return redirect('student_register') 

        return render(request, "student/student_register.html", {"form": form})
    

#Student job application


class StudentApplyJobView(View):
    template_name = "student/studentapplyjob.html"

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)

        # Pre-fill job field
        form = ApplicationForm(initial={"job": job})
        return render(request, self.template_name, {
            "form": form,
            "job": job
        })

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            student_name = "Vishnu Prasad"

            try:
                student = Student.objects.get(name=student_name)
            except Student.DoesNotExist:
                return redirect("job_list")

            application = form.save(commit=False)
            application.student = student
            application.job = job
            application.status = "Applied"
            application.save()

            # After success → back to job list
            return redirect("job_list")

        return render(request, self.template_name, {
            "form": form,
            "job": job
        })





    ###NEW 
class StudentJobListView(ListView):
    model = Job
    template_name = "student/Studentjoblist.html"
    context_object_name = "jobs"

    def get_queryset(self):
        queryset = Job.objects.select_related("job_type")
        job_type_id = self.request.GET.get("job_type")

        if job_type_id:
            queryset = queryset.filter(job_type_id=job_type_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_types"] = Jobtype.objects.all()
        context["selected_job_type"] = self.request.GET.get("job_type")
        return context   
    

from django.http import JsonResponse
from django.views import View

class StudentJobDetailView(View):
    def get(self, request, pk):
        job = Job.objects.get(pk=pk)
        data = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "salary": job.salary,
            "job_type": job.job_type.job_type,
        }
        return JsonResponse(data)


    
class StudentApplicationTrackingView(View):
    template_name = "student/studentapplicationtracking.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name")
        applications = None
        if name:
            applications = JobApplication.objects.filter(
                student__name__icontains=name
            ).select_related("job", "student").order_by("-applied_date")
        return render(request, self.template_name, {
            "applications": applications,
            "searched_name": name
        })
