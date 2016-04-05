"""
Django settings for sites project.

Generated by 'django-static-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import environ

root = environ.Path(__file__) - 3
base = environ.Path(__file__) - 2
# This points to the directory containing all the project code
SITE_ROOT = root()
BASE_ROOT = base()

env = environ.Env()
# reading .env file
environ.Env.read_env(os.path.join(SITE_ROOT, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'ci8',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    'staticsites',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sites.urls'

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
            # 'loaders': [
            #     'django.template.loaders.app_directories.Loader',
            # ],
        },
    },
]

WSGI_APPLICATION = 'sites.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# django-static-sites
FTP_STORAGE_LOCATION = ''

from django.core.files.storage import FileSystemStorage
from staticsites.conf_dict import DeployTypes
from storages.backends.ftp import FTPStorage

TEST_FTP_CONF = {
    'user': env('TEST_FTP_USER'),
    'password': env('TEST_FTP_PASSWORD'),
    'host': env('TEST_FTP_HOST'),
    'port': env('TEST_FTP_PORT'),
    'path': env('TEST_FTP_PATH'),
}
PROD_FTP_CONF = {
    'user': env('PROD_FTP_USER'),
    'password': env('PROD_FTP_PASSWORD'),
    'host': env('PROD_FTP_HOST'),
    'port': env('PROD_FTP_PORT'),
    'path': env('PROD_FTP_PATH'),
}

STATICSITE_DEPLOY_ROOT = DeployTypes({
    'dev': 'deploy/%(deploy_type)s',
    'test': 'ftp://%(user)s:%(password)s@%(host)s:%(port)s%(path)s' % TEST_FTP_CONF,
    'prod': 'ftp://%(user)s:%(password)s@%(host)s:%(port)s%(path)s' % PROD_FTP_CONF,
})

STATICSITE_DEFAULT_FILE_STORAGE = DeployTypes({
    'dev': FileSystemStorage,
    'test': FTPStorage,
    'prod': FTPStorage,
})

STATICSITE_GZIP = False
