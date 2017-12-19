import hashlib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
     hashlib.sha1(os.urandom(128)).hexdigest(), 
)

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost 127.0.0.1').split()

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',

    # Third party apps
    'rest_framework',
    'corsheaders',
    # Internal apps
    'myapp.apps.MyAppConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'myproject.urls'
WSGI_APPLICATION = 'wsgi.application'

from . import database

DATABASES = {
    'default': database.config()
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = False

PROJECT_LOGGING_LEVEL = os.getenv('PROJECT_LOGGING_LEVEL', 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(module)s:%(lineno)d:%(message)s'
            # 'format': '[%(levelname)s] [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': PROJECT_LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'project_logging': {
            'handlers': ['console',],
            'level': PROJECT_LOGGING_LEVEL,
        }
    }
}



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
            'rest_framework.renderers.JSONRenderer',)

# For using SSL with openshift
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# vim: ai et ts=4 sw=4 sts=4 nu ru
