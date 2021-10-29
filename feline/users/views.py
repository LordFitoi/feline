from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from feline.users.forms import SpanishPasswordChangeForm, SpanishPasswordChangeForm, SpanishSetPasswordForm, SpanishAuthenticationForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Información actualizada con exito  ")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class SpanishPasswordChangeView(PasswordChangeView):
    form = SpanishPasswordChangeForm


spanish_password_change_view = SpanishPasswordChangeView.as_view()


class SpanishLoginView(LoginView):
    form = SpanishAuthenticationForm


spanish_login_view = SpanishLoginView.as_view()


class SpanishPasswordResetConfirmView(PasswordResetConfirmView):
    form = SpanishSetPasswordForm


spanish_password_reset_confirm_view = SpanishPasswordResetConfirmView.as_view()