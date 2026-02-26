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
from users.forms import UserForm
from django.views.generic import TemplateView


from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from tims.users.models import User,Role
from users.forms import UserForm,LoginForm
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout


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


from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
#from faculty.models import TrainingSession,StudentAttendance

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


from users.forms import RoleForm

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
    
# #@login_required
# def role_based_redirect(request):
#     role = request.user.role.role_name

#     if role in ["Super Admin", "Admin", "HR", "Manager", "Faculty"]:
#         return redirect("staff_dashboard")

#     elif role == "Student":
#         return redirect("student_dashboard")

#     return redirect("login")    

# #@login_required
# def staff_dashboard(request):
#     return render(request, "users/staff_dashboard.html")
