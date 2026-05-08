#!/bin/bash
set -euo pipefail

extract_version() {

    if git describe --tags --exact-match 2>/dev/null; then
        git describe --tags --exact-match | sed 's/^backend-v//'
    else
        echo "0.0.0-$(git rev-parse --short HEAD)"
    fi
}


VERSION=$(extract_version)
GIT_SHA=$(git rev-parse --short HEAD)

REGISTRY="ghcr.io"
IMAGE_NAME="${REGISTRY}/hexyatina/catweek-backend"

echo "building image: ${IMAGE_NAME}:${VERSION}"

docker build \
  --tag "${IMAGE_NAME}:${VERSION}" \
  --tag "${IMAGE_NAME}:latest" \
  --build-arg VERSION="${VERSION}" \
  --build-arg GIT_SHA="${GIT_SHA}" \
  ./backend

echo "running smoke test..."
docker compose -f docker/docker-compose.ci.yaml up -d

MAX_RETRIES=15
COUNT=0
until curl -s -f http://localhost:5000/health > /dev/null || [ $COUNT -eq $MAX_RETRIES ]; do
    echo "Wait... ($((COUNT+1))/$MAX_RETRIES)"
    sleep 3
    COUNT=$((COUNT+1))
done

if [ $COUNT -eq $MAX_RETRIES ]; then
    echo "Smoke test failed!"
    docker compose -f docker/docker-compose.ci.yaml logs backend
    docker compose -f docker/docker-compose.ci.yaml down
    exit 1
fi

echo "Smoke test passed!"
docker compose -f docker/docker-compose.ci.yaml down

echo "CI Complete. Image ready:"
echo "  ${IMAGE_NAME}:${VERSION}"
echo "  ${IMAGE_NAME}:latest"