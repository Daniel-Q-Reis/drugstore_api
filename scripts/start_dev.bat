@echo off
echo Starting development containers (if not already running)...
docker-compose up -d
echo.
echo Your development environment is running.
echo Django is available at http://localhost:8000
echo Code changes will reload automatically.