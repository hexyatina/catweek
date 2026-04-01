#!/bin/sh
set -e

echo "Waiting for database..."
until uv run flask db current > /dev/null 2>&1; do
  echo "DB not ready yet - sleeping"
  sleep 2
done


echo "Running migrations..."
uv run flask db upgrade

echo "Seeding/Importing..."
uv run flask manage seed-if-empty
uv run flask manage import-schedule-yaml

echo "Starting server in $ENV mode..."
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}

if [ "$ENV" = "prod" ]; then
    exec uv run gunicorn --bind "$HOST:$PORT" --workers 4 wsgi:app
else
    exec uv run flask --app wsgi:app run --host "$HOST" --port "$PORT" --debug
fi