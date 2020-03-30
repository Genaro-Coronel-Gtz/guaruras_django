"""Using Django 1.11.4.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/
or the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'da2ej^ajsaty*4eh1gu+cawru(5fh4=ir-&va)ao%t90$=u6b2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']




# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
]

PROJECT_APPS = [
    'base',
    'usuarios', #1
    'servicios',#3
    'alertas',#2
    'utils'
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'guaruras.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'guaruras.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-ve'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

## Configuración de los directorios en donde se encuentran los archivos estáticos
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

## Configuración para el logeo de usuarios

LOGIN_URL = "/login"

LOGOUT_URL= "/logout"

# Configuración del rest framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

if 'DATABASE_URL' in os.environ:
    # Update database configuration with $DATABASE_URL.
    db_from_env = dj_database_url.config()
    DATABASES = {
        'default': db_from_env
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'ATOMIC_REQUESTS': True,
        }
    }
    #DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #        'NAME': 'guaruras',
    #        'USER': 'postgres',
    #        'PASSWORD': '',
    #        'HOST': 'localhost',
    #        'PORT': '',
    #        'ATOMIC_REQUESTS': True,
    #    }
    #}

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, '../static'),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Reset password
URL_RECOVER_PASS = 'front/url/forgot-password/'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ['EMAIL']
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASS']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = os.environ['EMAIL_PORT'] #587
EMAIL_USE_TLS = True
EMAIL_FROM = EMAIL_HOST_USER
