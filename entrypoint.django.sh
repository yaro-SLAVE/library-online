#!/bin/sh
set -e


echo "Fixing permissions..."
chown -R django:django /app/staticfiles /app/media

echo "Running migrations..."
python manage.py migrate --settings service_settings

echo "Initializing superuser..."
python manage.py init_superuser --settings service_settings \
    --username "${DJANGO_SUPERUSER_USERNAME}" \
    --password "${DJANGO_SUPERUSER_PASSWORD}" || echo "Superuser already exists or init failed"

if [ "$MODE" = "dev" ]; then
    echo "Starting development server as django user..."
    exec su django -c "python manage.py runserver 0.0.0.0:8000 --settings service_settings"
else
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --settings service_settings

    echo "Starting production server as django user..."
    export DJANGO_SETTINGS_MODULE=service_settings
    exec su django -c "uvicorn --host 0.0.0.0 --workers 4 app.asgi:application"
fi
