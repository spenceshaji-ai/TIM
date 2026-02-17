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




from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import UpdateView


from django.contrib import messages



from .forms import LoginForm, RegisterForm

from .forms import RoleForm









class LoginView(View):
    template_name = "users/login.html"

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
                login(request, user)

                # 🔥 Role Based Redirection
                if user.role and user.role.role_name in ["Admin", "HR"]:
                    return redirect("home")

                elif user.role and user.role.role_name == "Faculty":
                    return redirect("faculty:home1")

                # elif user.role and user.role.role_name == "Student":
                #     return redirect("student_dashboard")

                else:
                    return redirect("login")

        return render(request, self.template_name, {"form": form})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


# class RoleBasedRedirectView(View):
#     def get(self, request):
#         role = request.user.role.role_name

#         if role in ["Super Admin", "Admin", "HR", "Manager", "Faculty"]:
#             return redirect("users/staff_dashboard")

#         elif role == "Student":
#             return redirect("users/student_dashboard")

#         return redirect("users/login")


class RoleBasedRedirectView(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect("users:login")

        if not request.user.role:
            return redirect("users:login")

        role = request.user.role.role_name

        if role == "Super Admin":
            return redirect("users:superadmin_dashboard")

        elif role in ["Admin", "HR", "Manager"]:
            return redirect("users:admin_dashboard")

        elif role == "Faculty":
            return redirect("users:faculty_dashboard")

        elif role == "Student":
            return redirect("users:student_dashboard")

        return redirect("users:login")



class StaffDashboardView(View):
    def get(self, request):
        return render(request, "users/staff_dashboard.html")


class StudentDashboardView(View):
    def get(self, request):
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






# @method_decorator(login_required, name="dispatch")
# class UserListView(View):

#     def get(self, request):

#         # Role check
#         if not request.user.role or request.user.role.role_name not in ["Super Admin", "Admin"]:
#             return redirect("users:login")   # or redirect to dashboard

#         users = User.objects.select_related("role").all()
#         return render(request, "users/user_list.html", {"users": users})
class UserListView(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect("users:login")

        role_filter = request.GET.get("role")  # get role from URL

        users = User.objects.select_related("role").all()

        # 🎯 Apply filtering
        if role_filter == "student":
            users = users.filter(role__role_name__iexact="Student")

        elif role_filter == "faculty":
            users = users.filter(role__role_name__iexact="Faculty")

        elif role_filter == "staff":
            users = users.filter(role__role_name__in=["Admin", "HR", "Manager"])

        elif role_filter == "superadmin":
            users = users.filter(role__role_name__iexact="Super Admin")

        return render(request, "users/user_list.html", {"users": users})





