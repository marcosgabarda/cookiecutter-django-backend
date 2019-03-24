import warnings

import bleach
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

{%- if cookiecutter.use_celery == "y" %}
from {{ cookiecutter.project_slug }}.emails.tasks import send_email_asynchronously
{%- endif %}


class TemplateEmailMessage(object):
    """An object to handle emails based on templates, with automatic plain
    alternatives.
    """

    template_name = ""
    default_subject = ""
    default_from_email = ""
    fake = False

    def __init__(self, to, subject=None, context=None, from_email=None, attaches=None):
        if not self.template_name:
            warnings.warn('You have to specify the template_name')
        if not isinstance(to, list) and not isinstance(to, tuple):
            self.to = [to]
        self.subject = '%s' % self.default_subject if subject is None else subject
        self.from_email = self.default_from_email if from_email is None else from_email
        self.attaches = [] if attaches is None else attaches
        self.context = {} if context is None else context
        # Add default context
        current_site = Site.objects.get_current()
        self.context.update({
            "site": current_site,
        })

    def preview(self):
        """Renders the message for a preview."""
        message = render_to_string(self.template_name, self.context, using='django')
        return message

    {%- if cookiecutter.use_celery == "y" %}
    def async_send(self, message, message_txt):
        if not self.fake:
            send_email_asynchronously.delay(
                self.subject, message_txt, message, self.from_email, self.to
            )
            if self.attaches:
                warnings.warn('Attaches will not added to the email, use use_async=False to send attaches.')
    {%- endif %}

    def sync_send(self, message, message_txt):
        if not self.fake:
            email = EmailMultiAlternatives(
                subject=self.subject,
                body=message_txt,
                from_email=self.from_email,
                to=self.to
            )
            email.attach_alternative(message, "text/html")
            for attach in self.attaches:
                attach_file_name, attach_content, attach_content_type = attach
                email.attach(attach_file_name, attach_content, attach_content_type)
            email.send()

    def send(self{%- if cookiecutter.use_celery == "y" %}, use_async=True{%- endif %}):
        """Sends the email at the moment or using a Celery task."""
        if not settings.ENABLE_CUSTOM_EMAIL_SENDING:
            return
        message = render_to_string(self.template_name, self.context, using='django')
        message_txt = message.replace("\n", "")
        message_txt = message_txt.replace("</p>", "\n")
        message_txt = message_txt.replace("</h1>", "\n\n")
        message_txt = bleach.clean(message_txt, strip=True)

        {%- if cookiecutter.use_celery == "y" %}
        if use_async:
            self.async_send(message, message_txt)
        else:
            self.sync_send(message, message_txt)
        {% else %}
        self.sync_send(message, message_txt)
        {%- endif %}


class AdminsTemplateEmailMessage(TemplateEmailMessage):
    """Emails only for admins."""

    def __init__(self, subject=None, context=None, from_email=None):
        to = [a[1] for a in settings.ADMINS]
        super().__init__(to, subject=subject, context=context, from_email=from_email)


class ManagersTemplateEmailMessage(TemplateEmailMessage):
    """Emails only for mangers."""

    def __init__(self, subject=None, context=None, from_email=None):
        to = [a[1] for a in settings.MANAGERS]
        super().__init__(to, subject=subject, context=context, from_email=from_email)
