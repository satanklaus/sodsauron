from pathlib import Path
import ldap
import os
from django_auth_ldap.config import LDAPSearch

BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_URL = 'login'

SECRET_KEY = 'django-insecure-^$*+vzgw^97cqla=qjtug7!s_rx_rvd46cuy#sssmuh=p7x23t'

DEBUG = True

ALLOWED_HOSTS = ['eye.sodrk.ru']

INSTALLED_APPS = [
  'eye.apps.EyeConfig',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sauron.urls'

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

WSGI_APPLICATION = 'sauron.wsgi.application'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': str(BASE_DIR / 'db.sqlite3'),
  }
}

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


AUTH_LDAP_SERVER_URI = "ldap://10.149.0.209:389"

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'
LANGUAGES = [
  ('en', 'English'),
  ('ru', 'Russian')
]

LOCALE_PATHS = [
  './locale'
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
  "django_auth_ldap.backend.LDAPBackend",
  "django.contrib.auth.backends.ModelBackend"
]

AUTH_LDAP_SERVER_URI = "ldap://10.149.0.209"
AUTH_LDAP_BIND_DN = "CN=Kerberos,CN=Users,DC=sod,DC=local"
AUTH_LDAP_BIND_PASSWORD = "KerbAuth0"
AUTH_LDAP_USER_SEARCH = LDAPSearch("CN=Users,DC=sod,DC=local", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
  "username": "sAMAccountName",
  "first_name": "givenName",
  "last_name": "sn",
  "email": "mail",
}

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'file': {
      'level': 'DEBUG',
      'class': 'logging.FileHandler',
      'filename': '/var/log/uwsgi/sauron.debug.log',
    },
  },
  'loggers': {
    'django': {
      'handlers': ['file'],
      'level': 'DEBUG',
      'propagate': True,
    },
  },
}
