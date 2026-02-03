from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView, CreateView, DeleteView
from tims.users.models import User
from .forms import UserForm
from django.views.generic import TemplateView




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

#Role based redirect view

class RoleBasedRedirectView(LoginRequiredMixin, RedirectView):
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
class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/staff_dashboard.html"

# for student dashboard
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/student_dashboard.html"







# ✅ User List View
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

# ✅ Add User View
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_list")


# ✅ edit User View

class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_list")


# ✅ Delete User View
class UserDeleteView(DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")
