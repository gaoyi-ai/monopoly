from .base import *

DEBUG = False
ADMINS = (
    ('Yi Gao', '577981827@qq.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = ['39.105.184.237']
