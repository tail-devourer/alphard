from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from alphard.redis import redis
from utils.tasks import send_mail


class AccountActionEmailDispatcher:
    cooldown_seconds = 90
    redis_key_prefix = 'req-cool:'

    email_reverse = None
    email_subject = None
    email_template = None
    email_html_template = None

    def send_mail(self, request, user):
        if not redis.set(f'{self.redis_key_prefix}{user.pk}', '', ex=self.cooldown_seconds, nx=True):
            return False

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirmation_url = request.build_absolute_uri(
            reverse(self.email_reverse, kwargs={'uid': uid, 'token': token})
        )

        send_mail.delay(
            to=[user.email],
            subject=self.email_subject,
            template_name=self.email_template,
            html_template_name=self.email_html_template,
            context={
                'full_name': user.full_name,
                'confirmation_url': confirmation_url,
            },
        )

        return True
