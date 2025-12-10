#!/usr/bin/env bash
set -e

read_secret() {
    local name="$1"
    local prompt="${2:-}"
    local default="${3:-}"
    local auto_generate="${4:-false}"
    local value=""

    if [ "$auto_generate" = true ]; then
        value=$(LC_ALL=C tr -dc '!-~' < /dev/urandom | head -c 50)
    else
        if [ -n "$default" ]; then
            read -rp "$prompt (default: $default): " value
        else
            read -rp "$prompt: " value
        fi
        if [ -z "$value" ] && [ -n "$default" ]; then
            value="$default"
        fi
    fi

    if docker secret inspect "$name" >/dev/null 2>&1; then
        docker secret rm "$name" >/dev/null
    fi

    printf "%s" "$value" | docker secret create "$name" - >/dev/null
}

docker swarm init >/dev/null 2>&1 || true

read -rp "Is this a prod or test deployment (default: prod): " prod
prod=$(echo "$prod" | tr '[:upper:]' '[:lower:]' | xargs)

if [[ -z "$prod" || "$prod" == "prod" || "$prod" == "production" ]]; then
    csrf_cookie_secure="True"
    session_cookie_secure="True"
else
    csrf_cookie_secure="False"
    session_cookie_secure="False"
fi

if docker secret inspect alphard_csrf_cookie_secure >/dev/null 2>&1; then
    docker secret rm alphard_csrf_cookie_secure >/dev/null
fi

if docker secret inspect alphard_session_cookie_secure >/dev/null 2>&1; then
    docker secret rm alphard_session_cookie_secure >/dev/null
fi

printf "%s" "$csrf_cookie_secure" | docker secret create alphard_csrf_cookie_secure - >/dev/null
printf "%s" "$session_cookie_secure" | docker secret create alphard_session_cookie_secure - >/dev/null

read_secret "alphard_secret_key" "" "" true
read_secret "alphard_allowed_hosts" "Enter comma-separated list of domains allowed to serve the application"
read_secret "alphard_db_password" "" "" true

read_secret "alphard_email_host" "Enter SMTP server hostname"
read_secret "alphard_email_port" "Enter SMTP server port" "587"
read_secret "alphard_email_use_tls" "Do you want to enable TLS for outgoing emails?" "True"
read_secret "alphard_email_use_ssl" "Do you want to enable SSL for outgoing emails?" "False"
read_secret "alphard_email_host_user" "Enter SMTP username"
read_secret "alphard_email_host_password" "Enter SMTP password"
read_secret "alphard_default_from_email" "Enter default sender address for outgoing emails"

read_secret "alphard_admins" "Enter comma-separated list of name:email pairs for receiving admin error notifications"
read_secret "alphard_server_email" "Enter sender address used for system error emails to admins"

docker build -t alphard ./
docker stack deploy -c docker-stack.yml alphard
