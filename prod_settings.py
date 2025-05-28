from app.settings import *
import os

DEBUG = False

CSRF_TRUSTED_ORIGINS = [os.environ.get("SERVICE_CSRF_HOSTNAME")]
ALLOWED_HOSTS = [os.environ.get("SERVICE_HOSTNAME")]

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

OPAC_HOSTNAME = os.environ.get("OPAC_HOSTNAME")

OAUTH_CLIENT_ID = os.environ.get("OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.environ.get("OAUTH_CLIENT_SECRET")

OPAC_INTERNAL_TOKEN = os.environ.get("OPAC_INTERNAL_TOKEN")

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
