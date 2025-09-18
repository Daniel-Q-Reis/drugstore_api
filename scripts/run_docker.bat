@echo off

REM Start the services
docker-compose up -d

REM Wait for the database to be ready
echo Waiting for the database to be ready...
timeout /t 10 /nobreak >nul

REM Run migrations
docker-compose exec app python manage.py migrate

REM Create a superuser (optional)
REM docker-compose exec app python manage.py createsuperuser

echo The application is now running at http://localhost:8000