import os

from decouple import config

from .base import *  # noqa: F403

# SECURITY WARNING: keep the secret key used in production secret!
# In development, we can use a default value, but it must still come from environment variables
SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure-development-key-for-local-use-only"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "pharmacy_db"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React default port
    "http://127.0.0.1:3000",
]

# For development, you might want to allow all origins
# CORS_ALLOW_ALL_ORIGINS = True

# DRF Spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Pharmacy API",
    "DESCRIPTION": "A comprehensive pharmacy management system API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}
