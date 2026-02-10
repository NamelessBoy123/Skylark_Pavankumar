#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Pulling latest from git (main)..."
git pull origin main || true

echo "Building and starting containers..."
docker-compose up -d --build --remove-orphans

echo "Waiting for backend health (http://localhost:8000/health)..."
for i in {1..30}; do
  if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
    echo "Backend healthy."
    exit 0
  fi
  printf '.'
  sleep 2
done

echo "Warning: backend did not become healthy in time." >&2
docker-compose ps
docker-compose logs --tail=200 backend
exit 1
