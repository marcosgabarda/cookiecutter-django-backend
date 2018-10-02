from django.apps import AppConfig


class EmailsConfig(AppConfig):
    name = "{{ cookiecutter.project_slug }}.emails"
    verbose_name = "Emails"

    def ready(self):
        """Override this to put in:
            Emails system checks
            Emails signal registration
        """
        try:
            import emails.signals  # noqa F401
        except ImportError:
            pass
