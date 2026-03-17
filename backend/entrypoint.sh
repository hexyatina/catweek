#!/bin/sh
set -e

echo "Running migrations..."
uv run flask db upgrade

echo "Seeding database..."
uv run flask manage seed-if-empty

echo "Importing schedule..."
uv run flask manage import-schedule-yaml

echo "Starting server..."
if [ "$ENV" = "prod" ]; then
  exec uv run gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
else
  exec uv run flask --app wsgi:app run --host 0.0.0.0 --port 5000 --debug
fi