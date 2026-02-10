from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import RedirectView

#from django.views.generic import ListView, CreateView
from tims.users.models import User,Role
from .forms import UserForm
from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

from django.views.generic import UpdateView


from django.contrib import messages
from tims.users.models import User
from .forms import UserForm
from django.views.generic import TemplateView

from .forms import LoginForm, RegisterForm

from .forms import RoleForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user and user.status == "active":
                login(request, user)
                return redirect("role_redirect")

            return render(
                request,
                "users/login.html",
                {"form": form, "error": "Invalid credentials or inactive user"},
            )

        return render(request, "users/login.html", {"form": form})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
    

#@login_required
def role_based_redirect(request):
    role = request.user.role.role_name

    if role in ["Super Admin", "Admin", "HR", "Manager", "Faculty"]:
        return redirect("users/staff_dashboard")

    elif role == "Student":
        return redirect("users/student_dashboard")

    return redirect("users/login")


#@login_required
def staff_dashboard(request):
    return render(request, "users/staff_dashboard.html")


#@login_required
def student_dashboard(request):
    return render(request, "users/student_dashboard.html")



class UserRegisterView(View):
    template_name = "user_form.html"

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()
            print("USER SAVED:", user)

            messages.success(request, "Registration successful")
            #return redirect("login")   

        else:
            print("FORM ERRORS:", form.errors)   

        return render(request, self.template_name, {"form": form})



class RoleCreateView(View):
    template_name = "role_form.html"

    def get(self, request):
        form = RoleForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RoleForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Role created successfully")
            return redirect("users:role_add")

        return render(request, self.template_name, {"form": form})
