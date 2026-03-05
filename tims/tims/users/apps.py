from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tims.users"   # Python import path
    label = "users"       # ⭐ REQUIRED for AUTH_USER_MODEL
    verbose_name = _("Users")

    def ready(self):
        """
        Code to run when Django starts (optional)
        """
        pass