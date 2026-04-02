#!/bin/sh
set -e

echo "Waiting for database..."
MAX_WAIT=30
COUNT=0
until uv run python -c "import psycopg, os; psycopg.connect(os.environ['DATABASE_LOCAL'])" > /dev/null 2>&1; do
    if [ "$COUNT" -ge "$MAX_WAIT" ]; then
        echo "Database never became ready, exiting."
        exit 1
    fi
    echo "DB not ready yet - sleeping ($COUNT/$MAX_WAIT)"
    sleep 2
    COUNT=$((COUNT+1))
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