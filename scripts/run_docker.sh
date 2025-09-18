#!/bin/bash

# Start the services
docker-compose up -d

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
sleep 10

# Run migrations
docker-compose exec app python manage.py migrate

# Create a superuser (optional)
# docker-compose exec app python manage.py createsuperuser

echo "The application is now running at http://localhost:8000"