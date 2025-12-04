#!/bin/bash

set -e

: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"

while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" > /dev/null 2>&1; do
  sleep 1
done

export DEBUG=false
export SECRET_KEY=$(cat /run/secrets/django_secret_key)

export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export NPM_BIN_PATH=/usr/bin/npm

export REDIS_CACHE_URL=redis://redis:6379/0
export REDIS_URL=redis://redis:6379/1
export CELERY_BROKER_URL=redis://redis:6379/2
export CELERY_RESULT_BACKEND=redis://redis:6379/3

python manage.py migrate --noinput

exec "$@"
