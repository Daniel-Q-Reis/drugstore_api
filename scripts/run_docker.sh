#!/bin/bash

# Stop any running containers and remove volumes to ensure a clean start
echo "Performing a clean shutdown of existing containers..."
docker-compose down -v

# Start the services in detached mode
echo "Building and starting services..."
docker-compose up -d --build

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
sleep 10

# Run the unified setup command
echo "Running project setup (migrations, superuser, seeding)..."
docker-compose exec app python manage.py setup_project

echo "The application is now running at http://localhost:8000"