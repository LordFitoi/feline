from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class JobpostsConfig(AppConfig):
    name = 'feline.jobposts'
    verbose_name = _("Jobposts")
