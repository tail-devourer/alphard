"""Django settings generated using Django 6.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/6.0/ref/settings/

For deployment best practices and security checklist, see
https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
"""
import sys
import environ
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
SECRET_KEY_FALLBACKS = env.list('SECRET_KEY_FALLBACKS', default=[])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

if sys.platform == 'win32':
    NPM_BIN_PATH = env('NPM_BIN_PATH', default=r'C:\\Program Files\\nodejs\\npm.cmd')
else:
    NPM_BIN_PATH = env('NPM_BIN_PATH', default='/usr/bin/npm')

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True

    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

ROOT_URLCONF = 'alphard.urls'

TAILWIND_APP_NAME = 'theme'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'alphard.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='alphard'),
        'USER': env('DB_USER', default='alphard'),
        'PASSWORD': env('DB_PASS'),
        'HOST': env('DB_HOST', default='127.0.0.1'),
        'PORT': env.int('DB_PORT', default=5432),
    }
}

# Cache
# https://docs.djangoproject.com/en/6.0/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('CACHE_LOCATION', default='redis://127.0.0.1:6379/0'),
    }
}

# Sessions
# https://docs.djangoproject.com/en/6.0/topics/http/sessions/

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Redis

REDIS_URL = env('REDIS_URL', default='redis://127.0.0.1:6379/1')

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Celery

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://127.0.0.1:6379/2')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://127.0.0.1:6379/3')
CELERY_TIMEZONE = TIME_ZONE

# Email
# https://docs.djangoproject.com/en/6.0/topics/email/

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = env('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

MANAGERS = env.list('MANAGERS', default=[])
ADMINS = env.list('ADMINS', default=[])

# Static files
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'

# Media files
# https://docs.djangoproject.com/en/6.0/topics/files/

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

# Authentication
# https://docs.djangoproject.com/en/6.0/topics/auth/customizing/
AUTH_USER_MODEL = 'blog.CustomUser'
