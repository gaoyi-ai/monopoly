from .base import *

DEBUG = False
ADMINS = (
    ('Yi Gao', 'admin@qq.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Production mode specific
ALLOWED_HOSTS = ['127.0.0.1']
