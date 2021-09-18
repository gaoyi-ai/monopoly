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

ALLOWED_HOSTS = ['39.105.184.237', '3.18.221.239', '127.0.0.1']

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, '/static/'),
#     ]
