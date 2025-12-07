function Read-Secret {
    param(
        [Parameter(Mandatory=$true)]
        [string]$name,
        [string]$prompt = "",
        [string]$default = $null,
        [switch]$autoGenerate = $false
    )

    if ($autoGenerate) {
        $value = -join ((33..126) |
            Get-Random -Count 50 |
            ForEach-Object {[char]$_})
    } else {
        if ($default) {
            $value = Read-Host "$prompt (default - $default)"
        } else {
            $value = Read-Host $prompt
        }

        if ($value -eq "" -and $default) {
            $value = $default
        }
    }

    $value | docker secret create $name - | Out-Null
}

docker swarm init | Out-Null

$prod = Read-Host "Is this a prod or test deployment (default - prod)"
$prod = $prod.Trim().ToLower()

if ($prod -in @("", "prod")) {
    $csrf_cookie_secure = "True"
    $session_cookie_secure = "True"
} else {
    $csrf_cookie_secure = "False"
    $session_cookie_secure = "False"
}

$csrf_cookie_secure | docker secret create csrf_cookie_secure - | Out-Null
$session_cookie_secure | docker secret create session_cookie_secure - | Out-Null

Read-Secret -name "django_secret_key" -autoGenerate
Read-Secret -name "allowed_hosts" -prompt "Enter comma-separated list of domains allowed to serve the application"
Read-Secret -name "db_password" -autoGenerate

Read-Secret -name "email_host" -prompt "Enter SMTP server hostname"
Read-Secret -name "email_port" -prompt "Enter SMTP server port" -default "587"
Read-Secret -name "email_use_tls" -prompt "Do you want to enable TLS for outgoing emails?" -default "True"
Read-Secret -name "email_use_ssl" -prompt "Do you want to enable SSL for outgoing emails?" -default "False"
Read-Secret -name "email_host_user" -prompt "Enter SMTP username"
Read-Secret -name "email_host_password" -prompt "Enter SMTP password"
Read-Secret -name "default_from_email" -prompt "Enter default sender address for outgoing emails"

Read-Secret -name "admins" -prompt "[OPTIONAL] Enter comma-separated list of name:email pairs for receiving admin error notifications"
Read-Secret -name "server_email" -prompt "[OPTIONAL] Enter sender address used for system error emails to admins"

docker build -t alphard-web ./
docker build -t alphard-celery ./
docker build -t alphard-celery-beat ./

docker stack deploy -c docker-compose.yml alphard
