# Pharma-API: Django Pharmacy Management System

A comprehensive, robust RESTful API built with Django Rest Framework and PostgreSQL, designed to power a modern pharmacy management system.

This project provides real-time inventory control, tracks product expiration dates, and implements an intelligent, automatic promotion engine. It also features advanced reporting for stock value and sales velocity.

## Core Features

-   **Inventory Management**: Full CRUD operations for products, categories, and brands.
-   **Expiration Date Tracking**: Monitors product expiration dates to ensure safety and quality.
-   **Dynamic Pricing & Promotions**: Automatically applies progressive discounts (15%, 25%, 35%) as products approach their expiration dates (90, 60, 30 days).
-   **Advanced Reporting**: Endpoints to calculate the total financial value of the current stock, with filters for category and brand.
-   **Sales Velocity Tracking**: Analyzes sales data to report on how many units of a product were sold in the last 30 and 90 days.
-   **Data Seeding**: A custom management command to populate the database with realistic fake data for development and testing.
-   **Containerized Environment**: Fully containerized with Docker and Docker Compose for a consistent and reproducible setup.

## Technology Stack

-   **Backend**: Django, Django Rest Framework
-   **Database**: PostgreSQL
-   **Containerization**: Docker, Docker Compose
-   **Linting & Formatting**: Ruff
-   **Testing**: Pytest

## Getting Started

### Prerequisites

-   Docker
-   Docker Compose

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd pharma-api
    ```

2.  **Build and run the containers:**
    This command will build the Django image, start the application and the PostgreSQL database containers.
    ```bash
    docker-compose up --build -d
    ```

3.  **Apply database migrations:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4.  **(Optional) Populate the database with sample data:**
    ```bash
    docker-compose exec web python manage.py populate_db
    ```

The API should now be running and accessible at `http://localhost:8000`.

## API Endpoints

*(To be added once implemented)*

## Running Tests

*(To be added once implemented)*