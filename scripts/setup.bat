@echo off

REM Setup script for the Pharmacy API project on Windows

echo Setting up the Pharmacy API development environment...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install pre-commit hooks
echo Installing pre-commit hooks...
pre-commit install

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Create superuser if it doesn't exist
echo Creating superuser if it doesn't exist...
python manage.py createsuperuser_if_none_exists --username admin --email admin@example.com --password admin123

echo Setup complete! You can now run the development server with: python manage.py runserver