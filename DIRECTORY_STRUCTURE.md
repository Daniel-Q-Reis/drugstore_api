# Pharmacy API - Complete Directory Structure

pharmacy_api/
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── README.md
├── conftest.py
├── docker-compose.yml
├── manage.py
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── management/
│   │   │   ├── __init__.py
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       ├── createsuperuser_if_none_exists.py
│   │   │       └── seed_db.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_models.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── products/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── factories/
│   │   │   ├── __init__.py
│   │   │   └── factories.py
│   │   ├── models.py
│   │   ├── periodic_tasks.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── test_services.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── inventory/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── sales/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── factories/
│   │   │   ├── __init__.py
│   │   │   └── factories.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── test_services.py
│   │   ├── urls.py
│   │   └── views.py
│   └── reports/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests/
│       │   ├── __init__.py
│       │   └── test_models.py
│       ├── urls.py
│       └── views.py
├── pharmacy_api/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── schema.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
└── scripts/
    ├── setup.bat
    └── setup.sh