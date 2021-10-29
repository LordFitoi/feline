from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("Este nombre de usuario ya esta en uso.")}
        }

class SpanishAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Por favor introduzca un %(username)s y password. Recuerda que ambos "
            "campos pueden distinguir entre mayúsculas y minúsculas."
        ),
        'inactive': _("Esta cuenta esta inactiva."),
    }

class SpanishSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _('Los dos campos de password no son iguales.'),
    }


class SpanishPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Tu viejo password fue introducido incorrectamente. Por favor introducelo de nuevo."),
    }