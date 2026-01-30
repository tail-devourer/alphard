from redis import Redis
from django.conf import settings

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
