from .common_settings import * # noqa
from .common_settings import BASE_DIR
import os

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = ['.herokuapp.com']

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
