#!/bin/bash

set -e

if ! docker secret inspect django_secret_key >/dev/null 2>&1; then
  openssl rand 50 | docker secret create django_secret_key -
fi

if ! docker secret inspect db_password >/dev/null 2>&1; then
  openssl rand 20 | docker secret create db_password -
fi

docker compose up -d --build
