import json
from django.contrib.auth import get_user_model
from alphard.redis import redis

User = get_user_model()


class AuthEmailCooldownMixin:
    cooldown_seconds = 60
    redis_key_prefix = "auth-email-cooldown:"

    def start_email_cooldown(self, email, payload = {}):
        email = User.objects.normalize_email(email)
        redis.setex(f"{self.redis_key_prefix}{email}", self.cooldown_seconds, json.dumps(payload))

    def is_email_on_cooldown(self, email):
        email = User.objects.normalize_email(email)
        return redis.exists(f"{self.redis_key_prefix}{email}")

    def get_email_payload(self, email):
        email = User.objects.normalize_email(email)
        value = redis.get(f"{self.redis_key_prefix}{email}")
        return None if value is None else json.loads(value)
