from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from adminapp.models import FacultyAssignment
from .forms import FacultyCourseMaterialForm

class FacultyMaterialAddView(View):
    template_name = "course_material_form.html"

    def get(self, request):
        form = FacultyCourseMaterialForm(faculty=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = FacultyCourseMaterialForm(request.POST, request.FILES, faculty=request.user)
        if form.is_valid():
            material = form.save(commit=False)
            material.faculty = request.user  # assign logged-in faculty
            material.save()
            return redirect("faculty:material_add")  # redirect back to add page or list
        return render(request, self.template_name, {"form": form})

class Home1View(View):
    def get(self, request):
        return render(request, "home.html")