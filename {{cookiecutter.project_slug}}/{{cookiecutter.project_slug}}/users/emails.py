from django.utils.translation import ugettext_lazy as _

from {{ cookiecutter.project_slug }}.emails.helpers import TemplateEmailMessage


class VerificationEmail(TemplateEmailMessage):
    """Email notification when when an user is register, to verify his email."""

    template_name = "emails/verification.html"
    default_subject = _("Verify your email")


class RestorePasswordEmail(TemplateEmailMessage):
    """Email notification when when an user request a restore password code."""

    template_name = "emails/restore_password.html"
    default_subject = _("Restore your password")
