#!/bin/bash
set -e

# Build and start the containers in the background
docker compose up -d --build

# Give Postgres a beat to accept connections
sleep 5

# Run migrations inside the api container using `compose exec` so we don't
# have to hardcode the container name (which depends on the project directory)
docker compose exec api python manage.py makemigrations
docker compose exec api python manage.py migrate

echo "App is up. Hit it at http://localhost:8000"
