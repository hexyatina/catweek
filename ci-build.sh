#!/bin/bash
set -euo pipefail

OWNER="other-user" 
REPO="backend-app"
export IMAGE_NAME="ghcr.io/$OWNER/$REPO:local-test"

echo "building image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" ./backend

echo "running smoke test..."
docker compose -f docker/docker-compose.backend.yaml up -d

MAX_RETRIES=15
COUNT=0
until curl -s -f http://localhost:5000/ > /dev/null || [ $COUNT -eq $MAX_RETRIES ]; do
    echo "Wait... ($((COUNT+1))/$MAX_RETRIES)"
    sleep 3
    COUNT=$((COUNT+1))
done

if [ $COUNT -eq $MAX_RETRIES ]; then
    echo "Smoke test failed!"
    docker compose -f docker/docker-compose.backend.yaml logs backend
    docker compose -f docker/docker-compose.backend.yaml down
    exit 1
fi

echo "Smoke test passed!"
docker compose -f docker-compose.backend.yaml down

echo "CI Complete. Image $FULL_IMAGE is ready for registry."