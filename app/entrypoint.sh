#!/bin/sh

# Installer pg_dump si pas encore installé
apt-get update && \
apt-get install -y wget gnupg lsb-release && \
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
apt-get update && \
apt-get install -y postgresql-client-16 && \
ln -sf /usr/lib/postgresql/16/bin/pg_dump /usr/bin/pg_dump


# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start Celery workers and beat
celery -A project worker --loglevel=info &
celery -A project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Start Django server
exec python manage.py runserver 0.0.0.0:8000