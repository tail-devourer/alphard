docker swarm init

if (-not (docker secret ls | Select-String "django_secret_key")) {
    $secret = [System.Convert]::ToBase64String((1..50 | ForEach-Object { Get-Random -Maximum 256 }))
    Write-Output $secret | docker secret create django_secret_key -
}

if (-not (docker secret ls | Select-String "db_password")) {
    $db_pass = [System.Convert]::ToBase64String((1..20 | ForEach-Object { Get-Random -Maximum 256 }))
    Write-Output $db_pass | docker secret create db_password -
}

docker build -t alphard-web ./
docker build -t alphard-celery ./
docker build -t alphard-celery-beat ./

docker stack deploy -c docker-compose.yml alphard
