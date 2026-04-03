#!/bin/sh
set -e

echo "Starting backend in ${ENV} mode..."


echo "Waiting for database..."
uv run flask manage test-db-conn

echo "Running migrations..."
uv run flask db upgrade

echo "Seeding/Importing..."
uv run flask manage seed-if-empty
uv run flask manage import-schedule-yaml

echo "Starting server in $ENV mode..."

if [ "$ENV" = "prod" ]; then
    echo "Running Gunicorn (production)"
    exec uv run gunicorn \
        --bind "0.0.0.0:${PORT}" \
        --workers "${WORKERS:-4}" \
        --timeout 120 \
        wsgi:app
else
    echo "Running Flask dev server"
    exec uv run flask --app wsgi:app run \
        --host "0.0.0.0" \
        --port "${PORT}" \
        --debug
fi