#!/bin/bash
set -euo pipefail

REGISTRY="ghcr.io"
IMAGE_NAME="${REGISTRY}/hexyatina/catweek-backend"
COMPOSE_FILE="docker/docker-compose.ci.yaml"

cleanup() {
    echo "Cleaning up..."
    docker compose -f "${COMPOSE_FILE}" down --volumes 2>/dev/null || true
}
trap cleanup EXIT

extract_version() {
    local tag
    if tag=$(git describe --tags --exact-match 2>/dev/null); then
        echo "${tag#backend-v}"
    else
        echo "0.0.0-$(git rev-parse --short HEAD)"
    fi
}

VERSION=$(extract_version)
GIT_SHA=$(git rev-parse --short HEAD)

echo "Building image: ${IMAGE_NAME}:${VERSION}"

docker build \
    --tag "${IMAGE_NAME}:${VERSION}" \
    --tag "${IMAGE_NAME}:latest" \
    --build-arg VERSION="${VERSION}" \
    --build-arg GIT_SHA="${GIT_SHA}" \
    ./backend

echo "Running smoke test..."

IMAGE_NAME="${IMAGE_NAME}:latest" \
    docker compose -f "${COMPOSE_FILE}" up -d --wait

curl -sf http://localhost:5000/health | jq .
curl -sf http://localhost:5000/ready | jq .

echo "Smoke test passed!"
echo "Image ready:"
echo "  ${IMAGE_NAME}:${VERSION}"
echo "  ${IMAGE_NAME}:latest"