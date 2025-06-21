import os
from pathlib import Path
import environ

# Настройка переменных окружения через .env
env = environ.Env(
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent  

# Загрузка .env-файла
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Секреты и настройки среды
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

INSTALLED_APPS = [
    # Приложения Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REST Framework и сторонние
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',
    'channels',
    'django_filters',

    # Моё приложение
    'LabaWeb',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'LabaWeb.middleware.ActionLoggingMiddleware', # Пользовательское логирование
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'
ASGI_APPLICATION = 'main.asgi.application'

# Настройка базы данных через env
DATABASES = {
    'default': env.db(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# CORS
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_CREDENTIALS = env.bool('CORS_ALLOW_CREDENTIALS', default=True)

# Сессии
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SAMESITE = 'Lax'  
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_SAVE_EVERY_REQUEST = True

# Медиа-файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Локализация и часовой пояс
LANGUAGE_CODE = 'ru-ru'  
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статика
STATIC_URL = '/static/'