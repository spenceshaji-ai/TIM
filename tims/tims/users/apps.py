from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "tims.users"
    verbose_name = _("Users")

    def ready(self):
        """
        Override this method in subclasses to run code when Django starts.
        """
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tims.users"   # the Python module path
    label = "users"       # 👈 the app_label Django uses for models