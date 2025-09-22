# Pharmacy API

A comprehensive pharmacy management system API built with Django REST Framework, designed with enterprise-level standards for quality, security, and maintainability.

## Features

- **Robust Architecture**: Built on Clean Architecture principles with a dedicated Service Layer and Data Transfer Objects (DTOs) to ensure separation of concerns.
- **User Authentication**: Secure JWT-based authentication with a custom user model.
- **Product Management**: Complete CRUD for brands, categories, products, and stock items.
- **Sales Management**: Transactional sales creation with automatic stock updates and dynamic discount calculations.
- **Inventory Tracking**: Real-time inventory management with expiration date tracking.
- **Advanced Reporting**: Endpoints for sales summaries, inventory value, and financial insights.
- **High Performance**: Caching strategies with Redis to optimize frequent queries.
- **Asynchronous Tasks**: Celery and Redis for handling background processes and scheduled tasks.
- **Comprehensive Testing**: Full test suite covering unit, integration, and service layers using `pytest` and `factory-boy`.
- **Automated Quality & Security**: CI/CD pipeline with GitHub Actions that runs linters (`ruff`), static type checking (`mypy --strict`), and security scanning (`bandit`).
- **Interactive API Documentation**: Auto-generated, interactive API documentation with Swagger UI and ReDoc via `drf-spectacular`.

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Caching & Task Queues**: Redis
- **Background Tasks**: Celery
- **API Documentation**: drf-spectacular
- **Testing**: pytest, factory-boy, Faker
- **Code Quality**: `black`, `ruff`, `mypy`, `pre-commit`, `bandit`
- **Deployment**: Docker, Docker Compose, Gunicorn

---

## 🚀 Getting Started with Docker

This is the recommended method for running the project, as it provides a consistent environment.

### Prerequisites

- Docker
- Docker Compose

### Automated Setup (Recommended)

A single script will build the containers, run database migrations, create a default superuser, and seed the database with sample data.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd pharmacy_api
    ```

2.  **Create your local environment file:**
    ```bash
    cp .env.example .env
    ```
    *(You can customize variables inside `.env` if needed, but the defaults work out-of-the-box.)*

3.  **Run the setup script:**
    -   On **Unix/Linux/Mac**:
        ```bash
        scripts/run_docker.sh
        ```
    -   On **Windows**:
        ```bat
        scripts\run_docker.bat
        ```

This process will execute the `setup_project` command, which:
-   Applies all database migrations.
-   Creates a default superuser.
    -   **Username**: `admin`
    -   **Email**: `admin@example.com`
    -   **Password**: `admin123`
-   Seeds the database with a generous amount of sample data. To run the setup *without* seeding the database, execute: `docker-compose exec app python manage.py setup_project --no-seed`

### Manual Setup (For More Control)

If you prefer to run each step manually:

1.  **Build and start the services:**
    ```bash
    docker-compose up --build -d
    ```
2.  **Run migrations:**
    ```bash
    docker-compose exec app python manage.py migrate
    ```
3.  **Create a superuser:**
    ```bash
    docker-compose exec app python manage.py createsuperuser_if_none_exists
    ```
4.  **(Optional) Seed the database:**
    ```bash
    docker-compose exec app python manage.py seed_db
    ```

### Accessing the Application

Once the application is running, the following endpoints will be available:

-   **Django Admin**: `http://localhost:8000/admin`
    -   *Login with the superuser credentials (`admin@example.com` / `admin123`)*.

-   **API Documentation (Swagger UI)**: `http://localhost:8000/api/v1/schema/swagger-ui/`
    -   *The best place to explore and test the API endpoints interactively.*

-   **API Documentation (ReDoc)**: `http://localhost:8000/api/v1/schema/redoc/`
    -   *Alternative documentation view.*

-   **API Base Path**: `http://localhost:8000/api/v1/`
    -   *Note: This is the base prefix for all API endpoints (e.g., `/api/v1/products/`, `/api/v1/sales/`). It does not have a user interface and will show a 404 error if accessed directly in a browser.*

To shut down the services, run: `docker-compose down`. For a clean shutdown that also removes the database volume, use `docker-compose down -v`.

---

## 🧪 Testing & Code Quality

This project is configured with a strict set of quality gates to ensure code is reliable and maintainable.

### Running Tests

Execute the entire test suite with `pytest`:

```bash
pytest
```
To generate a detailed coverage report in HTML format:

```bash
pytest --cov=. --cov-report=html
```

Code Quality Checks
The project uses pre-commit to automate quality checks before every commit. To run all checks manually across the entire codebase:

```bash
pre-commit run --all-files
```
This will execute the following tools:

black: For uncompromising code formatting.

ruff: An extremely fast linter for identifying potential bugs and style issues.

mypy: A static type checker running in strict mode to enforce type safety.

bandit: A security scanner to find common security vulnerabilities.

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

## License & Contact
This project is licensed under the MIT License.

Author: Daniel de Queiroz Reis

Email: danielqreis@gmail.com

WhatsApp: +55 35 99190-2471