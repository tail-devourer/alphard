FROM python:3.14-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV NPM_BIN_PATH=/usr/bin/npm

RUN apt update
RUN apt install -y gcc build-essential libpq-dev python3 \
  python3-dev python3-pip curl
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
RUN apt install -y nodejs
RUN rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install gunicorn
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py tailwind install
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
