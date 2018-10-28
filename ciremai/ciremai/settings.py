"""
Django settings for ciremai project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dare7z2*px2lwmab_(04ghyt4s)2f8g!&oo^66n$f6!20@l#=r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
SITE_TITLE = 'ciremai'

ANONYMOUS_USER_ID = -1
AUTH_USER_MODEL = "auth.User"

LOGIN_URL = "/inventory/login/"
LOGIN_URL_BILLING = "/billing/login/"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    #
    'crispy_forms',
    'datetimewidget',
    'django_tables2',
    'bootstrap3',
    'avatar',
    'annoying',
    'simple_history',
    'widget_tweaks',
    'mptt',
    'django_select2',
    'rest_framework',
    'corsheaders',
    #'dal',
    #'dal_select2',
    #
    'inventory',
    'billing',
    'middleware',
    #'pa',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ciremai.urls'


REST_FRAMEWORK = {
 'DEFAULT_PERMISSION_CLASSES': [
 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
 ]
}
CORS_ORIGIN_WHITELIST = (
 '127.0.0.1:8080',
 'localhost:8080',
)

#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

#########################
# CIREMAI CONFIGURATION #
#########################

# HL7 Message
HL7_ORDER_DIR = 'C:\\HL7'

# report file
RESULT_REPORT_FILE_HEADER = 'D:\\git\\ciremai\\report_jrxml\\ciremaiHeader.jrxml'
RESULT_REPORT_FILE_MAIN = 'D:\\git\\ciremai\\report_jrxml\\ciremaiReport.jrxml'
RESULT_REPORT_FILE = 'D:\\git\\ciremai\\report_jrxml\\ciremaiReport.jasper'
RESULT_REPORT_DIR = 'D:\\git\\ciremai\\report_jrxml'

REPORT_DIR = 'D:\\git\\ciremai\\report_jrxml\\out'
# Jasper Report Database
JASPER_CONN = {
        'driver': 'mysql',
        'username': 'root',
        'password': 'P455word',
        'host': '127.0.0.1',
        'database': 'db_gs'
    }

#########################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, "templates"),
            ],
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

WSGI_APPLICATION = 'ciremai.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'db_gs',
        'USER': 'root',
        'PASSWORD': 'P455word',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'id'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True

AVATAR_AUTO_GENERATE_SIZES = (60,)
AVATAR_PROVIDERS = (
    'avatar.providers.PrimaryAvatarProvider',
    #'avatar.providers.GravatarAvatarProvider',
    'avatar.providers.DefaultAvatarProvider',
)
AVATAR_DEFAULT_URL = 'http://127.0.0.1:8000/media/avatars/avatar.jpg'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

CRISPY_TEMPLATE_PACK="bootstrap3"

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    'D:\\git\\ciremai\\ciremai\\static',
]

#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = 'D://git//ciremai//ciremai//media'
MEDIA_URL = '/media/'

#PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
#PROJECT_DIR = 'D://git//ciremai//ciremai//'
#STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

#print STATIC_ROOT





