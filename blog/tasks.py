from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_confirmation_email(full_name, email, confirmation_url):
    context = {
        "full_name": full_name,
        "confirmation_url": confirmation_url
    }

    text_body = render_to_string("email/confirm-email.txt", context)
    html_body = render_to_string("email/confirm-email.html", context)

    msg = EmailMultiAlternatives(
        subject="Confirm your email",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()
