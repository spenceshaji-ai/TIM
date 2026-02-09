from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from tims.users.models import User
from .forms import UserForm
from django.views.generic import TemplateView
from tims.users.models import User,Role


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


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

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})

user_redirect_view = UserRedirectView.as_view()

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
