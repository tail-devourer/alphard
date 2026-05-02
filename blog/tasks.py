from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def send_mail(to, subject, template_name, html_template_name, context):
    text_body = render_to_string(template_name, context)
    html_body = render_to_string(html_template_name, context)

    msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, to)
    msg.attach_alternative(html_body, 'text/html')
    msg.send()
