# core/settings.py
from pathlib import Path

import boto3

ssm_client = boto3.client('ssm')


def get_parameter(name, with_decryption=True):
    return ssm_client.get_parameter(Name=name, WithDecryption=with_decryption)['Parameter']['Value']


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_parameter('/swift_order/api/DJANGO_SECRET_KEY')
DEBUG = bool(get_parameter('/swift_order/api/DEBUG'))
ALLOWED_HOSTS = [get_parameter('/swift_order/api/ALLOWED_HOSTS')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd Party Apps
    "rest_framework",
    "corsheaders",
    # 1st Party Apps
    "customers.apps.CustomersConfig",
    "products.apps.ProductsConfig",
    "orders.apps.OrdersConfig",
    "pdfs.apps.PdfsConfig",
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

CORS_ALLOW_ALL_ORIGINS = bool(get_parameter('/swift_origin/api/CORS_ALLOW_ALL_ORIGINS'))

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_parameter('/swift_order/api/DB_NAME'),
        'USER': get_parameter('/swift_order/api/DB_USER'),
        'PASSWORD': get_parameter('/swift_order/api/DB_PASSWORD'),
        'HOST': get_parameter('/swift_order/api/DB_HOST'),
        'PORT': get_parameter('/swift_order/api/DB_PORT'),
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom Settings
AWS_PRESIGNED_URL_EXPIRATION = get_parameter('/swift_order/api/AWS_PRESIGNED_URL_EXPIRATION')
AWS_STORAGE_BUCKET_NAME = get_parameter('/swift_order/api/AWS_STORAGE_BUCKET_NAME')
WHATSAPP_API_TOKEN = get_parameter('/swift_order/api/WHATSAPP_API_TOKEN')
WHATSAPP_PHONE_NUMBER = get_parameter('/swift_order/api/WHATSAPP_PHONE_NUMBER')
WHATSAPP_API_URL = get_parameter('/swift_order/api/WHATSAPP_API_URL')
