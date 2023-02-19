import os

from neonlush.settings import BASE_DIR

DEBUG = False  # Production ortamında DEBUG kesinlikle kapatılmalıdır ki saldırganlar site hakkında detaylı hata raporlarına ulaşamasınlar.

ALLOWED_HOSTS = ['alanadi.com', '192.168.1.10']  # I

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
