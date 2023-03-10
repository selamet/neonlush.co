import os
import warnings

from django.core.management.utils import get_random_secret_key

from neonlush.settings import BASE_DIR

SECRET_KEY = os.environ.get("SECRET_KEY", "thisissecretkey")
DEBUG = os.environ.get("DEBUG", True)

if not SECRET_KEY:
    warnings.warn("SECRET_KEY not configured, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ORIGIN_ALLOW_ALL = True

STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/www/static/',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
