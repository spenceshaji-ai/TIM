from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from adminapp.models import Course,Batch
from .forms import CourseForm,BatchForm

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


#class FacultyAssignmentCreateView(View):
  #  def get(self, request):
        form = FacultyAssignmentForm()
        return render(request, "adminapp/faculty_assignment.html", {
            "form": form
        })

   # def post(self, request):
        form = FacultyAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminapp:faculty_assignment")

        return render(request, "adminapp/faculty_assignment.html", {
            "form": form
        })
