# Pharmacy API

A comprehensive pharmacy management system API built with Django REST Framework.

## Features

- **User Authentication**: JWT-based authentication with custom user model
- **Product Management**: Complete CRUD operations for brands, categories, products, and stock items
- **Sales Management**: Create sales with automatic stock updates and discount calculations
- **Inventory Tracking**: Real-time inventory management with expiration date tracking
- **Reporting**: Sales summaries, inventory reports, and financial insights
- **Caching**: Redis-based caching for improved performance
- **Asynchronous Tasks**: Celery for background processing and scheduled tasks
- **API Documentation**: Interactive API documentation with Swagger UI and ReDoc
- **Testing**: Comprehensive test suite with pytest and factory-boy
- **Code Quality**: Pre-commit hooks with Black, Flake8, and isort

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Caching**: Redis
- **Background Tasks**: Celery
- **API Documentation**: drf-spectacular
- **Testing**: pytest, factory-boy, Faker
- **Code Quality**: Black, Flake8, isort, pre-commit
- **Deployment**: Docker, Docker Compose, Gunicorn

## Installation

### Prerequisites

- Python 3.11
- Docker and Docker Compose
- PostgreSQL (if running without Docker)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pharmacy_api
   ```

2. Run the setup script:
   ```bash
   # On Windows
   scripts\setup.bat
   
   # On Unix/Linux/Mac
   bash scripts/setup.sh
   ```

3. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Using Docker

1. Build and start services:
   ```bash
   docker-compose up --build
   ```

2. Run migrations:
   ```bash
   docker-compose exec app python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   docker-compose exec app python manage.py createsuperuser
   ```

4. Access the application:
   - API: http://localhost:8000/
   - Swagger UI: http://localhost:8000/api/v1/schema/swagger-ui/
   - ReDoc: http://localhost:8000/api/v1/schema/redoc/

### Switching Between Docker and Local Development

To run the application locally without Docker:

1. Make sure you have Python 3.11 and PostgreSQL installed on your system.

2. Create a PostgreSQL database:
   ```sql
   CREATE DATABASE pharmacy_db;
   CREATE USER postgres WITH PASSWORD 'postgres';
   GRANT ALL PRIVILEGES ON DATABASE pharmacy_db TO postgres;
   ```

3. Update the `pharmacy_api/settings/development.py` file to use your local PostgreSQL instance:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'pharmacy_db',
           'USER': 'postgres',
           'PASSWORD': 'postgres',
           'HOST': 'localhost',  # Changed from 'db' to 'localhost'
           'PORT': '5432',
       }
   }
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

For convenience, you can use the provided scripts:
- On Windows: `scripts\run_docker.bat` to start with Docker, `scripts\stop_docker.bat` to stop
- On Unix/Linux/Mac: `scripts/run_docker.sh` to start with Docker, `scripts/stop_docker.sh` to stop

To easily switch between Docker and local development settings:
- On Windows: `scripts\use_local_settings.bat` to switch to local development, `scripts\use_docker_settings.bat` to switch back to Docker
- On Unix/Linux/Mac: `scripts/use_local_settings.sh` to switch to local development, `scripts/use_docker_settings.sh` to switch back to Docker

## API Documentation

Once the server is running, you can access the API documentation:

- **Swagger UI**: http://localhost:8000/api/v1/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/v1/schema/redoc/

## Testing

Run the test suite with pytest:
```bash
pytest
```

Generate a coverage report:
```bash
pytest --cov-report=html --cov=.
```

## Code Quality

Run code quality checks:
```bash
# Run all linters
pre-commit run --all-files

# Or run individually
black .
flake8 .
isort .
```

## Seeding Data

To seed the database with sample data:
```bash
python manage.py seed_db
```

## Environment Variables

Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Key variables:
- `DEBUG`: Set to `True` for development, `False` for production
- `SECRET_KEY`: Django secret key
- `DB_*`: Database connection settings
- `REDIS_URL`: Redis connection URL
- `CELERY_*`: Celery broker and result backend settings

## Project Structure

```
pharmacy_api/
├── apps/
│   ├── core/          # Core app with management commands
│   ├── users/         # User management and authentication
│   ├── products/      # Product and inventory management
│   ├── sales/         # Sales and transaction management
│   └── reports/       # Reporting and analytics
├── pharmacy_api/      # Main project settings and configuration
├── scripts/           # Setup and utility scripts
└── requirements.txt   # Python dependencies
```

## License

This project is licensed under the MIT License.