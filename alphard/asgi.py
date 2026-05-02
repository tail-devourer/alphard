"""ASGI config to expose the ASGI callable as a module-level variable named ``application``."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alphard.settings')
application = get_asgi_application()
