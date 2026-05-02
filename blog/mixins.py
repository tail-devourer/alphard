from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from alphard.redis import redis
from .tasks import send_mail

class AccountActionEmailDispatcher:
    cooldown_seconds = 120
    redis_key_prefix = 'req-cool:'

    action_url_name = None
    email_subject = None
    email_template = None
    email_html_template = None

    def dispatch(self, request, user):
        if not redis.set(f'{self.redis_key_prefix}{user.pk}', '', ex=self.cooldown_seconds, nx=True):
            return False

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        action_url = request.build_absolute_uri(
            reverse(self.action_url_name, kwargs={'uid': uid, 'token': token})
        )

        send_mail.delay(
            user.email,
            self.email_subject,
            self.email_template,
            self.email_html_template,
            {
                'full_name': user.full_name,
                'action_url': action_url
            }
        )

        return True
