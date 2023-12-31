#!/bin/bash

docker-compose down

echo "docker compose down completed"

docker volume rm littlelemon_little_db

echo "docker docker volume cleared"

docker-compose up --build -d

echo "Running tests..."
docker exec -it little-app python manage.py test
