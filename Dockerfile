FROM python:3.14-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NPM_BIN_PATH=/usr/bin/npm

RUN apt update \
    && apt install -y gcc build-essential libpq-dev python3-dev curl postgresql-client \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | sh - \
    && apt install -y nodejs

COPY ./requirements.txt .
RUN pip install gunicorn \
    && pip install -r requirements.txt

COPY . .

RUN python manage.py tailwind install \
    && python manage.py tailwind build \
    && python manage.py collectstatic --noinput

RUN rm -r ./theme/static_src
RUN apt purge -y gcc build-essential libpq-dev python3-dev curl nodejs \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
