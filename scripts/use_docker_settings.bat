@echo off

REM Switch to Docker settings
echo Switching to Docker settings...

REM Check if backup file exists
if exist "pharmacy_api\settings\development.py.docker.bak" (
    REM Restore the Docker settings from backup
    copy "pharmacy_api\settings\development.py.docker.bak" "pharmacy_api\settings\development.py"
    del "pharmacy_api\settings\development.py.docker.bak"
    echo Successfully switched to Docker settings.
) else (
    REM Update the development.py file to use 'db' instead of localhost for PostgreSQL
    powershell -Command "(gc pharmacy_api\settings\development.py) -replace "'HOST': 'localhost'", "'HOST': 'db'" | Out-File -encoding ASCII pharmacy_api\settings\development.py"
    echo Successfully switched to Docker settings.
)