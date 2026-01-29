

# Create your views here.
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from Admin.models import Job
from .forms import JobForm

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
    






