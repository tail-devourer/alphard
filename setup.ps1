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
            $value = Read-Host "$prompt (default: $default)"
        } else {
            $value = Read-Host $prompt
        }

        if ($value -eq "" -and $default) {
            $value = $default
        }
    }

    docker secret inspect $name 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        docker secret rm $name | Out-Null
    }

    $value | docker secret create $name - | Out-Null
}

docker swarm init | Out-Null

Read-Secret -name "alphard_enable_ssl" -prompt "Enforce HTTPS and HSTS" -default "True"
Read-Secret -name "alphard_secret_key" -autoGenerate
Read-Secret -name "alphard_allowed_hosts" -prompt "Enter comma-separated list of domains allowed to serve the application"
Read-Secret -name "alphard_db_password" -autoGenerate

Read-Secret -name "alphard_email_host" -prompt "Enter SMTP server hostname"
Read-Secret -name "alphard_email_port" -prompt "Enter SMTP server port" -default "587"
Read-Secret -name "alphard_email_use_tls" -prompt "Do you want to enable TLS for outgoing emails?" -default "True"
Read-Secret -name "alphard_email_use_ssl" -prompt "Do you want to enable SSL for outgoing emails?" -default "False"
Read-Secret -name "alphard_email_host_user" -prompt "Enter SMTP username"
Read-Secret -name "alphard_email_host_password" -prompt "Enter SMTP password"
Read-Secret -name "alphard_default_from_email" -prompt "Enter default sender address for outgoing emails"

Read-Secret -name "alphard_admins" -prompt "Enter comma-separated list of name:email pairs for receiving admin error notifications"
Read-Secret -name "alphard_server_email" -prompt "Enter sender address used for system error emails to admins"

docker build -t alphard ./

docker stack deploy -c docker-stack.yml alphard
