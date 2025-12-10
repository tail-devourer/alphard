#!/bin/bash

echo "Waiting for postgres to be ready..."
while ! pg_isready -h alphard_db -p 5432 > /dev/null 2>&1; do
  sleep 1
done

echo "Applying migrations..."
python manage.py migrate --noinput

exec "$@"
