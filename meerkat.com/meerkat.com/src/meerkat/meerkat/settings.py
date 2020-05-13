# -*- coding: utf-8 -*-
"""
Django settings for meerlat project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: meerkat.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (ROOT_PATH + '/templates',)
MEDIA_ROOT = ROOT_PATH + '/media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

#문자인코딩 방식으로 인한 에러를 막기위해 추가됨. 오류로 표시되어도 제대로 작동함.
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm6_#w*(l-zzql-39bu=tx^g^-kiphrxy_r=wx6)24jxfrk++c6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'custom_user',
    'common',
    'knowledge',
    'crawler',
)

#for custom_user app (using email to primary key)
AUTH_USER_MODEL = 'custom_user.EmailUser'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'meerkat.urls'

WSGI_APPLICATION = 'meerkat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'meerkat',
        'USER': 'postgres',
        'PASSWORD': '00000NUL(null)',
        'HOST':'192.168.0.4',
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,
                }
             }
         
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
DATABASE_OPTIONS = {'charset': 'utf8'}

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
