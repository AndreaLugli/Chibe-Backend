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
	'django_celery_beat',
	'social_django',
	'staff',
	'snowpenguin.django.recaptcha2'
]

RECAPTCHA_PUBLIC_KEY = '6LdvTEEUAAAAAAeRFNkxinkmyW5v76nzBzpvKC0w'
RECAPTCHA_PRIVATE_KEY = '6LdvTEEUAAAAAO4INyat5h6ZuOJSAE189JiKkZgS'

AUTHENTICATION_BACKENDS = [
	'main.views.CustomGooglePlusAuth',
	'social_core.backends.facebook.FacebookOAuth2',
	'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_FACEBOOK_KEY = '1610936385616742'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b91d4828bab3e99a4c6f2cf1b08b0c80'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'it_IT',
  'fields': 'id, name, email, first_name, last_name'
}

SOCIAL_AUTH_GOOGLE_PLUS_KEY = '700637450112-on9jl395jvl3ann7oioj1ab488imob8h.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'eXh6xNiY3_IbklplkiAhQBRq'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'main.views.register_social',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

FIELDS_STORED_IN_SESSION = ['token']

SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['user_code']


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
	'chibe.middleware.CheckAuth',
	#'chibe.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'chibe.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
			    'social_django.context_processors.backends',
			    'social_django.context_processors.login_redirect',

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
	from settings_production import *


