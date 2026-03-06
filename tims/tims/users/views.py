
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
from django.contrib.auth import authenticate, login
from django.contrib import messages




from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import UpdateView


from django.contrib import messages



from .forms import LoginForm, RegisterForm

from .forms import RoleForm
from django.contrib.auth import login








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
                    return redirect("superadmin:home5")   # or superadmin dashboard

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




class RoleCreateView(View):
    template_name = "role_form.html"

    def get(self, request):

        # Only Superadmin and Admin can access
        if not request.user.is_authenticated:
            return redirect("login")

        form = RoleForm()
        return render(request, self.template_name, {"form": form})



    def post(self, request):

        if not request.user.is_authenticated:
            return redirect("login")

        form = RoleForm(request.POST)

        if form.is_valid():

            role_name = form.cleaned_data["role_name"]

            # ⭐ SUPERADMIN can create Admin, HR, Manager
            if request.user.is_superuser:
                if role_name not in ["Admin", "HR", "Manager"]:
                    messages.error(request, "Superadmin can only create Admin, HR, Manager roles")
                    return redirect("users:role_add")

            # ⭐ ADMIN can create Student, Faculty
            elif request.user.role.role_name == "Admin":
                if role_name not in ["Student", "Faculty"]:
                    messages.error(request, "Admin can only create Student and Faculty roles")
                    return redirect("users:role_add")

            else:
                messages.error(request, "You are not allowed to create roles")
                return redirect("login")

            form.save()
            messages.success(request, "Role created successfully")
            return redirect("users:role_add")

        return render(request, self.template_name, {"form": form})
