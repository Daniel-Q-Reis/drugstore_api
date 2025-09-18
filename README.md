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