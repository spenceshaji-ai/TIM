from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from tims.users.models import User


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

class TrainingSessionCreate(View):
    template_name = 'training/create_session.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': TrainingSessionForm(),
            'title': 'Create Training Session'
        })

    def post(self, request):
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_list')
        return render(request, self.template_name, {
            'form': form,
            'title': 'Create Training Session'
        })
class TrainingSessionList(View):
    template_name = 'Session_list.html'

    def get(self, request):
        sessions = (
            TrainingSession.objects
            .select_related('batch', 'faculty')
            .order_by('-session_date')
        )
        return render(request, self.template_name, {
            'sessions': sessions
        })
class TrainingSessionUpdate(View):
    template_name = 'update_session.html'

    def get(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        return render(request, self.template_name, {
            'form': TrainingSessionForm(instance=session),
            'title': 'Update Training Session'
        })

    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('training_list')
        return render(request, self.template_name, {
            'form': form,
            'title': 'Update Training Session'
        })
                
class TrainingSessionDelete(View):

    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        session.delete()
        return redirect('training_list')


training_session_delete_view = TrainingSessionDelete.as_view()
       

