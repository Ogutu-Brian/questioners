"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import django_heroku
import logging
import environ
from django.utils.translation import gettext_lazy as _
import os

# Project Base Paths
# project_root/api/config/settings.py - 3 = project_root/
ROOT_DIR = environ.Path(__file__) - 3
API_DIR = ROOT_DIR.path('api')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load OS environment variables and then prepare to use them
env = environ.Env()
DJANGO_ENV = env.str('DJANGO_ENV', default='development')

# Loading .env file from root directory to set environment.
# OS Environment variables have precedence over variables defined
# in the .env file, that is to say variables from the .env files
# will only be used if not defined as environment variables.
env_file = ROOT_DIR('.env')
env.read_env(env_file)

if DJANGO_ENV == 'development':
    # SECURITY WARNING: don't run with debug turned on in production!
    # https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-DEBUG

    DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
# https://docs.djangoproject.com/en/2.0/ref/settings/#secret-key

SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# Hosts/domain names that are valid for this site
# https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
USE_X_FORWARDED_HOST = env.bool('DJANGO_USE_X_FORWARDED_HOST', default=True)

# Django Installed Apps
# https://docs.djangoproject.com/en/2.0/ref/settings/#installed-apps

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'macros',
    'users',
    'meetups',
    'djoser',
    'mail_templated',
    'utils',
    'django_filters',
    'django_extensions',
    'django.contrib.postgres',
    'phonenumber_field',
    'rest_framework_swagger',
]

# Rest Framework Settings
# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':
    ('rest_framework.permissions.DjangoModelPermissions', ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': env.str(
            'DJANGO_DEFAULT_THROTTLE_RATE_ANON', default='60/minute'),
        'user': env.str(
            'DJANGO_DEFAULT_THROTTLE_RATE_USER', default='120/minute'),
    },
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':
    env.int('DJANGO_DEFAULT_PAGE_SIZE', default=25),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'EXCEPTION_HANDLER':
    'config.exceptions.api_exception_handler',
}

# Djoser Auth Related Settings
# http://djoser.readthedocs.io/en/latest/settings.html

DJOSER = {
    'LOGIN_URL': 'login',
    'PASSWORD_RESET_CONFIRM_URL': 'auth/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'auth/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SEND_ACTIVATION_SMS': True,
    'SEND_CONFIRMATION_SMS': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'LOGOUT_ON_PASSWORD_CHANGE': True,
}

# Django Middlewares
# https://docs.djangoproject.com/en/2.0/topics/http/middleware/

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Root url config entry point
# https://docs.djangoproject.com/en/2.0/ref/settings/#root-urlconf

ROOT_URLCONF = 'config.urls'

# Django Template Configuration
# https://docs.djangoproject.com/en/2.0/ref/settings/#templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [API_DIR('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]

# Path to the WSGI Application Object
# https://docs.djangoproject.com/en/2.0/ref/settings/#wsgi-application

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': '',
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = env.int(
    'DATABASE_CONN_MAX_AGE', default=0)

# Caching Settings
# https://docs.djangoproject.com/en/2.0/topics/cache/

REDIS_LOCATION = '{0}/{1}'.format(
    env.str('REDIS_URL', default='redis://127.0.0.1:6379'), 0)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}

# Custom User Model
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Sites Framework
# https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SITE_ID

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'
LOCALE_PATHS = [
    API_DIR('locale'),
    API_DIR('contrib/rest_framework/locale'),
    API_DIR('contrib/auth/locale'),
    API_DIR('contrib/conf/locale'),
]
USE_I18N = True
USE_L10N = True

# Timezone settings
# https://docs.djangoproject.com/en/2.0/topics/i18n/timezones/

TIME_ZONE = 'UTC'
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = API_DIR('static')
STATICFILES_DIRS = [
    os.path.join(API_DIR('assets'), 'static'),
]
STATIC_URL = '/static/'

# User uploaded media files
# https://docs.djangoproject.com/en/2.0/topics/files/

MEDIA_ROOT = API_DIR('media')
MEDIA_URL = '/media/'
# Site Specific Settings

DOMAIN = env.str('DOMAIN', default='localhost:3000')
SITE_NAME = _(env.str('SITE_NAME'))
SITE_LOGO_URL = env.str('SITE_LOGO_URL')
SITE_OWNER_NAME = _(env.str('SITE_OWNER_NAME'))
SITE_OWNER_URL = env.str('SITE_OWNER_URL')
ADMIN_SITE_HEADER = env.str('ADMIN_SITE_HEADER')
API_BROWSER_HEADER = env.str('API_BROWSER_HEADER')

# Celery Settings
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

CELERY_BROKER_URL = REDIS_LOCATION
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Email Settings
# https://docs.djangoproject.com/en/2.0/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = env.str('EMAIL_USE_TLS', default='')
EMAIL_HOST = env.str('EMAIL_SMTP_HOST', default='localhost')
EMAIL_HOST_USER = env.str('EMAIL_SMTP_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_SMTP_PASSWORD', default='')
EMAIL_PORT = env.int('EMAIL_SMTP_PORT', default=1025)

# Prefix for emails to administrators
EMAIL_SUBJECT_PREFIX = '[ADMIN] '

# Default from emails
DEFAULT_FROM_EMAIL = _(env.str('DEFAULT_FROM_EMAIL'))
SERVER_EMAIL = _(env.str('DEFAULT_SERVER_EMAIL'))

# Sms Settings

SENDSMS_BACKEND = 'sendsms.backends.console.SmsBackend'
SENDSMS_FROM_NUMBER = "+XXxxxxxxxxxx"
SENDSMS_ACCOUNT_SID = 'ACXXXXXXXXXXXXXX'
SENDSMS_AUTH_TOKEN = 'xxxxxxxx'

# Mobile Auth Token Settings
MOBILE_DAILY_TOKEN_REQUEST_LIMIT = 50
MOBILE_TOKEN_ATTEMPT_LIMIT = 10
MOBILE_ACTIVATION_TOKEN_LENGTH = 6
MOBILE_ACTIVATION_TOKEN_HASH_ALGORITHM = 'sha256'

# Test Settings
TEST_PAYLOAD_PATH = str(API_DIR) + '/utils/test/'
TEST_DATA_PATH = TEST_PAYLOAD_PATH + 'data/'

# Site Reliability Team
# https://docs.djangoproject.com/en/2.0/ref/settings/#admins

ADMINS = [('Django', 'drf@email.com')]
MANAGERS = [('Django', 'drf@email.com')]

# Exported settings available in templates
# https://github.com/jakubroztocil/django-settings-export

SETTINGS_EXPORT = [
    'DOMAIN',
    'SITE_NAME',
    'ADMIN_SITE_HEADER',
    'API_BROWSER_HEADER',
]

# Deployment checklist should be visited before deployment to production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

if DJANGO_ENV == 'production':
    # Sentry Client for Application Logging in Production
    # See https://docs.sentry.io/clients/python/integrations/django/
    INSTALLED_APPS += ['raven.contrib.django.raven_compat']
    RAVEN_MIDDLEWARE = [
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware'
    ]
    MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE

    # Sentry Configuration
    SENTRY_DSN = env.str('DJANGO_SENTRY_DSN')
    SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': [
                'sentry',
            ],
        },
        'formatters': {
            'verbose': {
                'format':
                '%(levelname)s %(asctime)s %(module)s '
                '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level':
                'ERROR',
                'class':
                'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': [
                    'console',
                ],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': [
                    'console',
                ],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': [
                    'console',
                ],
                'propagate': False,
            },
            'django.security.DisallowedHost': {
                'level': 'ERROR',
                'handlers': [
                    'console',
                    'sentry',
                ],
                'propagate': False,
            },
        },
    }
    SENTRY_CELERY_LOGLEVEL = env.int(
        'DJANGO_SENTRY_LOG_LEVEL', default=logging.INFO)
    RAVEN_CONFIG = {
        'CELERY_LOGLEVEL':
        env.int('DJANGO_SENTRY_LOG_LEVEL', default=logging.INFO),
        'DSN':
        SENTRY_DSN
    }

django_heroku.settings(locals())
del DATABASES['default']['OPTIONS']['sslmode']
