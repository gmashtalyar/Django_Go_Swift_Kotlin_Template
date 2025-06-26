from pathlib import Path
import os, sys
from firebase_admin import initialize_app, credentials

BASE_DIR_docs = Path(__file__).resolve(strict=True).parent.parent
MEDIA_URL = '/Documents/'
MEDIA_ROOT = os.path.join(BASE_DIR_docs, "Documents")
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ['django_key']

DEBUG = True

ALLOWED_HOSTS = []
# CSRF_TRUSTED_ORIGINS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'swift',
    'main_app',
    'fcm_django'
]

ASGI_APPLICATION = "WebTemplate.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WebTemplate.urls'

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

WSGI_APPLICATION = 'WebTemplate.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': os.environ.get('DB_PORT'),
#     }
# }

# docker run --name test_db -e POSTGRES_DB=test_db_name -e POSTGRES_USER=test_db_user -e POSTGRES_PASSWORD=test_db_password -p 5432:5432 -d postgres
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db_name',
        'USER': 'test_db_user',
        'PASSWORD': 'test_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


LANGUAGE_CODE = 'Ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "mail.hosting.reg.ru"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEIGHBORING_DIR = os.path.join(BASE_DIR, 'certificates')
cred = credentials.Certificate(os.path.join(NEIGHBORING_DIR, 'firebase_service_account.json'))
FIREBASE_APP = initialize_app(cred, options={'max_workers': 50})


# FCM_DJANGO_SETTINGS = {
#     "FCM_SERVER_KEY": os.environ.get('FCM_SERVER_KEY')
# }
