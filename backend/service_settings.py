from app.settings import *
import os

DEBUG = os.environ.get("DEBUG", "0") == "1"

# Validate required environment variables
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY must be set in environment variables")

# Filter out None values for ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS
service_hostname = os.environ.get("SERVICE_HOSTNAME")
service_csrf_hostname = os.environ.get("SERVICE_CSRF_HOSTNAME")

ALLOWED_HOSTS = [service_hostname] if service_hostname else []
CSRF_TRUSTED_ORIGINS = [service_csrf_hostname] if service_csrf_hostname else []

OPAC_HOSTNAME = os.environ.get("OPAC_HOSTNAME", "")

OAUTH_CLIENT_ID = os.environ.get("OAUTH_CLIENT_ID", "")
OAUTH_CLIENT_SECRET = os.environ.get("OAUTH_CLIENT_SECRET", "")

OPAC_INTERNAL_TOKEN = os.environ.get("OPAC_INTERNAL_TOKEN", "")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": "5432",
    }
}
