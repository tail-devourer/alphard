#!/bin/bash

echo "Waiting for postgres to be ready..."
while ! pg_isready -h alphard_db -p 5432 > /dev/null 2>&1; do
  sleep 1
done

export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

echo "Applying migrations..."
python manage.py migrate --noinput

exec "$@"
