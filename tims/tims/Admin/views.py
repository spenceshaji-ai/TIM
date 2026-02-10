

# Create your views here.
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from Admin.models import Job,Jobtype
from .forms import JobForm,JobtypeForm

from Student.models import JobApplication
from  Admin.models import Interview
from .forms import ScheduleInterviewForm
from django.utils import timezone





class JobtypeCreateView(View):
    def get(self, request):
        form = JobtypeForm()
        return render(request, "admin/jobtype_create.html", {"form": form})

    def post(self, request):
        form = JobtypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jobtype_list')  # Redirect to list page after save
        return render(request, "admin/jobtype_create.html", {"form": form})
    

class JobtypeListView(View):
    def get(self, request):
        jobtypes = Jobtype.objects.all()  # get all Jobtype entries
        return render(request, "admin/jobtype_list.html", {"jobtypes": jobtypes})

class JobtypeEditView(View):
    def get(self, request, pk):
        jobtype = get_object_or_404(Jobtype, pk=pk)
        form = JobtypeForm(instance=jobtype)
        return render(request, "admin/jobtype_edit.html", {"form": form, "jobtype": jobtype})

    def post(self, request, pk):
        jobtype = get_object_or_404(Jobtype, pk=pk)
        form = JobtypeForm(request.POST, instance=jobtype)
        if form.is_valid():
            form.save()
            return redirect("jobtype_list")  # Redirect back to list after saving
        return render(request, "admin/jobtype_edit.html", {"form": form, "jobtype": jobtype})
    
class JobtypeDeleteView(View):
    def get(self, request, pk):
        jobtype = get_object_or_404(Jobtype, pk=pk)
        return render(request, "admin/jobtype_delete.html", {"jobtype": jobtype})

    def post(self, request, pk):
        jobtype = get_object_or_404(Jobtype, pk=pk)
        jobtype.delete()
        return redirect("jobtype_list")

# Manual CBVs using View

# CREATE JOB

class JobCreateView(View):
    def get(self, request):
        form = JobForm()
        return render(
            request,
            'admin/job_create.html',
            {'form': form}
        )

    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')

        return render(
            request,
            'admin/job_create.html',
            {'form': form}
        )


# LIST JOBS

class JobListView(View):
    def get(self, request):
        jobs = Job.objects.all()
        return render(
            request,
            'admin/job_list.html',
            {'jobs': jobs}
        )


# EDIT JOB

class JobEditView(View):
    def get(self, request, id):
        job = get_object_or_404(Job, id=id)
        form = JobForm(instance=job)
        return render(
            request,
            'admin/job_edit.html',
            {'form': form, 'job': job}
        )

    def post(self, request, id):
        job = get_object_or_404(Job, id=id)
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect('job_list')

        return render(
            request,
            'admin/job_edit.html',
            {'form': form, 'job': job}
        )


# DELETE JOB

class JobDeleteView(View):
    def get(self, request, id):
        job = get_object_or_404(Job, id=id)
        return render(
            request,
            'admin/job_delete.html',
            {'job': job}
        )

    def post(self, request, id):
        job = get_object_or_404(Job, id=id)
        job.delete()
        return redirect('job_list')
    


class AdminApplicationListView(View):
    def get(self, request):
        applications = JobApplication.objects.select_related(
            'job', 'student'
        ).order_by('-applied_date')

        current_time = timezone.now()

        return render(request, 'admin/application_list.html', {
            'applications': applications,
            'current_time': current_time
        })

class AdminApplicationShortlistView(View):
    def post(self, request, id):
        application = get_object_or_404(JobApplication, id=id)
        if application.status == "Applied":
            application.status = "Shortlisted"
            application.save()
        return redirect('admin_application_list')

class AdminApplicationRejectView(View):
    def post(self, request, id):
        application = get_object_or_404(JobApplication, id=id)
        application.status = "Rejected"
        application.save()
        return redirect('admin_application_list')
    


class AdminApplicationSelectView(View):
    def post(self, request, id):
        application = get_object_or_404(JobApplication, id=id)
        if application.status == "Interview":
            application.status = "Selected"
            application.save()
        return redirect('admin_application_list')


class ScheduleInterviewView(View):
    template_name = "admin/schedule_interview.html"

    def get(self, request, application_id):
        application = get_object_or_404(JobApplication, id=application_id)
        # If interview exists, prevent editing
        if hasattr(application, 'interview'):
            return redirect('admin_application_list')

        form = ScheduleInterviewForm()
        return render(request, self.template_name, {'form': form, 'application': application})

    def post(self, request, application_id):
        application = get_object_or_404(JobApplication, id=application_id)
        if hasattr(application, 'interview'):
            return redirect('admin_application_list')

        form = ScheduleInterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.status = 'Scheduled'
            interview.save()

            # Update JobApplication status
            application.status = 'Interview'
            application.save()
            return redirect('admin_application_list')

        return render(request, self.template_name, {'form': form, 'application': application})
    


    
#Tracking the Applications

# def JobApplicationTracking(request):
#     applications = JobApplication.objects.select_related('job', 'student')
#     return render(request, 'admin/JobApplicationTracking.html', {
#         'applications': applications
#     })

# #Tracking the Applications Status

# def JobApplicationTrackingstatus(request, pk, status):
#     application = get_object_or_404(JobApplication, pk=pk)

#     allowed_statuses = ['Shortlisted', 'Interview', 'Selected', 'Rejected']

#     if status in allowed_statuses:
#         application.status = status
#         application.save()

#     return redirect('applicationtracking_list')