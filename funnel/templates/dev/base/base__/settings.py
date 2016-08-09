"""
Django settings for dealerfunnel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIRS = (
                  os.path.join(BASE_DIR, 'templates'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0_m21^3$k5^!*n9j_i6)p2pt)n6bbw)4^()0(cu6t52v1sc-ka'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'dealerfunnel.funnel',
    'south'
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dealerfunnel.urls'

WSGI_APPLICATION = 'dealerfunnel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#database

DATABASES = {
    'default': {
        'NAME': 'admin_funnel',
        'ENGINE': 'django.db.backends.mysql',
        'USER': "geoffkhalid",
        'PASSWORD': "xD?i057j",
        'HOST': "205.186.143.147",
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
    }
}

'''
DATABASES = {
    'default': {
        'NAME': 'dealerfunnel',
        'ENGINE': 'django.db.backends.mysql',
        'USER': "root",
        'PASSWORD': "123456",
        'HOST': "localhost",
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
    }
}
'''
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_USE_TLS = True

EMAIL_HOST = 'dealerfunnel.com'

EMAIL_HOST_USER = 'admin@dealerfunnel.com'

EMAIL_HOST_PASSWORD = 'Xcel_2005'

EMAIL_PORT = 25

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'statics')

STATIC_URL = '/statics/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'staticfiles'),
)
