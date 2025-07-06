#!/bin/bash

# Ждем, пока база данных будет готова
echo "Waiting for database..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $POSTGRES_USER
do
  sleep 2
done

echo "Database is ready!"

# Выполняем миграции
echo "Running migrations..."
python manage.py migrate

# Исправляем права на static директории
echo "Fixing permissions on static directories..."
sudo chown -R appuser:appuser /app/static/backend/ || true
sudo chown -R appuser:appuser /app/media/ || true

# Собираем статические файлы
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Запускаем сервер
echo "Starting server..."
gunicorn --bind 0.0.0.0:8000 foodgram_backend.wsgi:application 