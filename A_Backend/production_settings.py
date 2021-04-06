from .common_settings import *
import os

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = ['.herokuapp.com']

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

