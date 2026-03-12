from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView, CreateView, DeleteView
from tims.users.models import User
from .forms import UserForm
from django.views.generic import TemplateView


from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from tims.users.models import User
from tims.faculty.models import FacultyCourseMaterial
from .forms import UserForm, LoginForm
from django.views.generic import TemplateView
from tims.users.models import User,Role
from django.contrib.auth import authenticate, login,logout


# class UserDetailView(LoginRequiredMixin, DetailView):
#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"


# user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        user = self.request.user

        if user.role and user.role.role_name == "Faculty":
            return reverse("faculty:dashboard")

        elif user.role and user.role.role_name == "Admin":
            return reverse("adminapp:home")

        elif user.role and user.role.role_name == "Student":
            return reverse("student:home")

        return reverse("users:login")






class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:

                  # 🔐 1️⃣ INACTIVE CHECK (ADD HERE)
                if user.status != "active":
                    messages.error(request, "Your account is inactive")
                    return redirect("login")
                login(request, user)
                 # ⭐ FORCE PASSWORD CHANGE (ADD HERE)
                if user.must_change_password and not user.is_superuser:
                    return redirect("users:change_password")
               
                # 🔥 Role Based Redirection
                  # 🔥 SUPER ADMIN CHECK
                if user.is_superuser:
                    return redirect("adminapp:home2")   # or superadmin dashboard

                if user.role and user.role.role_name in ["Admin", "HR","Manager"]:
                    return redirect("adminapp:home2")

                elif user.role and user.role.role_name == "Faculty":
                    return redirect("faculty:home1")

                elif user.role and user.role.role_name == "Student":
                    return redirect("Student:stdhome")

                else:
                    messages.error(request, "Role not assigned properly")
                    return redirect("login")
        messages.error(request, "Invalid username or password")
        return render(request, self.template_name, {"form": form})


class ForcePasswordChangeView(View):

    template_name = "change_password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("users:change_password")

        user = request.user

        user.set_password(password1)

        user.must_change_password = False

        user.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # ROLE BASED REDIRECT
        if user.role:
            role = user.role.role_name

            if role == "Admin":
                return redirect("adminapp:home2")

            elif role == "HR":
                return redirect("adminapp:home2")

            elif role == "Manager":
                return redirect("adminapp:home2")

            elif role == "Faculty":
                return redirect("faculty:home1")

            elif role == "Student":
                return redirect("Student:stdhome")

        return redirect("login")

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")

    def get(self, request):
        return render(request, "logout.html")


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


from .forms import RoleForm

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
    
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class RoleBasedLoginView(LoginView):
    template_name = "users/login.html"  # your login template

    def get_success_url(self):
        user = self.request.user

        if user.role and user.role.role_name == "Faculty":
            return reverse_lazy("faculty:dashboard")

        elif user.role and user.role.role_name == "Admin":
            return reverse_lazy("adminapp:home")

        elif user.role and user.role.role_name == "Student":
            return reverse_lazy("student:home")

        return reverse_lazy("users:redirect")  # fallback
    

class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                # 🔥 Role Based Redirection
                if user.role and user.role.role_name in ["Admin", "HR"]:
                    return redirect("adminapp:home2")

                elif user.role and user.role.role_name == "Faculty":
                    return redirect("faculty:home1")

                elif user.role and user.role.role_name == "student":
                     return redirect("Student:stdhome")

                else:
                    return redirect("login")

        return render(request, self.template_name, {"form": form})
