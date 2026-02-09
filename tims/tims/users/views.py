from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import RedirectView

from django.views.generic import ListView, CreateView
from tims.users.models import User,Role
#from .forms import UserForm
from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

from .models import User, Role
from .forms import LoginForm, RegisterForm

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # default status = active
            user.status = "active"
            user.set_password(form.cleaned_data["password1"])
            user.save()

            login(request, user)
            return redirect("role_redirect")

        return render(request, "users/register.html", {"form": form})

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




"""(class UserDetailView( DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView( SuccessMessageMixin, UpdateView):
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


class UserRedirectView( RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()



#Role based redirect view

class RoleBasedRedirectView( RedirectView):
    permanent = False

    def get_redirect_url(self):

        role = self.request.user.role.role_name

        # SAME template for Admin, SuperAdmin, Faculty
        if role in ["Super Admin", "Admin", "Faculty", "HR", "Manager"]:
            return reverse("staff_dashboard")

        # DIFFERENT template for Student
        elif role == "Student":
            return reverse("student_dashboard")

        return reverse("home")
role_redirect_view = RoleBasedRedirectView.as_view()

#for view admindashboard
class StaffDashboardView( TemplateView):
    template_name = "dashboards/staff_dashboard.html"

# for student dashboard
class StudentDashboardView( TemplateView):
    template_name = "dashboards/student_dashboard.html"







# ✅ User List View
class UserListView( ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

# ✅ Add User View
class UserCreateView( CreateView):
    model = User
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_list")


# ✅ edit User View

class UserEditView( UpdateView):
    model = User
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_list")


# ✅ Delete User View
class UserDeleteView(DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user_list") )"""
