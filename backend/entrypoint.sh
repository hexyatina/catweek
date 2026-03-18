#!/bin/sh
set -e

echo "Running migrations..."
uv run flask db upgrade

echo "Seeding database..."
uv run flask manage seed-if-empty

echo "Importing schedule..."
uv run flask manage import-schedule-yaml

echo "Starting server..."
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}

if [ "$ENV" = "prod" ]; then
    exec uv run gunicorn --bind "$HOST:$PORT" --workers 4 wsgi:app
else
    exec uv run flask --app wsgi:app run --host "$HOST" --port "$PORT" --debug
fi