from celery.task import task
from django.core.mail import EmailMultiAlternatives


@task(serializer='json')
def send_email_asynchronously(subject, message_txt, message, from_email, to):
    """Sends an email as a asynchronous task."""
    email = EmailMultiAlternatives(
        subject=subject,
        body=message_txt,
        from_email=from_email,
        to=to
    )
    email.attach_alternative(message, "text/html")
    email.send()
