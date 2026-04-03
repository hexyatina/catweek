#!/bin/sh
set -e

echo "Starting backend in ${ENV} mode..."

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}
WORKERS=${WORKERS:-4}


echo "Waiting for database..."

until uv run python -c "
import sqlalchemy as sa
from app.config import settings
print(f'DEBUG: Attempting connection to: {settings.DATABASE_URL_DIRECT.split(\"@\")[-1]}') # Hide password, show host
engine = sa.create_engine(settings.DATABASE_URL_DIRECT)
with engine.connect() as conn:
    conn.execute(sa.text('SELECT 1'))
    print('DEBUG: Connection successful!')
"; do
  echo "Remote database not reachable - retrying in 3s..."
  sleep 3
done

echo "Running migrations..."
uv run flask db upgrade

echo "Seeding/Importing..."
uv run flask manage seed-if-empty
uv run flask manage import-schedule-yaml

echo "Starting server in $ENV mode..."

if [ "$ENV" = "prod" ]; then
    echo "Running Gunicorn (production)"
    exec uv run gunicorn \
        --bind "$HOST:$PORT" \
        --workers "$WORKERS" \
        --timeout 120 \
        --access-logfile - \
        --error-logfile - \
        wsgi:app
else
    echo "Running Flask dev server"
    exec uv run flask --app wsgi:app run \
        --host "$HOST" \
        --port "$PORT" \
        --debug
fi