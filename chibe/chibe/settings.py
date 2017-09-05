from django.contrib.messages import constants as messages
import os
import socket
local_name = socket.gethostname()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '033kmmu)ihh*sgv&9v7y%9fb5-z5al!vorefc7h_()@+82o#o_'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'corsheaders',
	'azienda',
	'main',
	'desideri',
	'django_celery_results',
	'django_celery_beat'
]


CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'pickle' 
CELERY_ACCEPT_CONTENT = ['pickle']

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chibe.urls'

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

WSGI_APPLICATION = 'chibe.wsgi.application'

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

LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

ADMINS = (
	('Riccardo Russo', 'senblet@gmail.com'),
)

MANAGERS = ADMINS
SERVER_EMAIL = 'chibe@chibeapp.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.chibeapp.com'
EMAIL_HOST_USER = 'chibe@chibeapp.com'
EMAIL_HOST_PASSWORD = 'sf3o4ow%tdfbxcv4675ioerj'
EMAIL_PORT = 587

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


if (local_name == "Riccardos-MacBook-Pro.local") or (local_name == "Riccardos-MBP") or (local_name == "Riccardos-MBP.lan") or (local_name == "Riccardos-MBP.station"):
	from settings_locale import *
else:
	from settings_dev import *


