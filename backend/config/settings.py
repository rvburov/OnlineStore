# Импорт стандартных библиотек и модулей для работы с окружением
import os
from pathlib import Path
from decouple import config  # Импорт библиотеки для управления переменными окружения

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ приложения, считываемый из переменных окружения
SECRET_KEY = config('SECRET_KEY')

# Режим отладки: включается/выключается через переменные окружения
DEBUG = True

# Разрешенные хосты для развертывания проекта
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Доверенные источники для CSRF-токенов
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='').split(',')

# Список приложений Django (встроенные)
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Локальные приложения проекта (созданные пользователем)
LOCAL_APPS = [
    'debug_toolbar',
]

# Сторонние приложения, установленные через pip
THIRD_PARTY_APPS = [
    'users',
    'orders',
    'catalog',
    'cart',
    'homepages',
    'core',
]

# Полный список установленных приложений
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

# Список middleware для обработки запросов/ответов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Middleware для отладки
]

# Корневая конфигурация URL
ROOT_URLCONF = 'config.urls'

# Настройки шаблонов Django
TEMPLATES_DIR = BASE_DIR / 'templates'  # Каталог с пользовательскими шаблонами
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],  # Указываем директорию шаблонов
        'APP_DIRS': True,  # Включение автоматического поиска шаблонов в приложениях
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Дополнительный процессор для корзины
                'cart.context_processors.cart_total_items',
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = 'config.wsgi.application'

# Настройки базы данных (SQLite по умолчанию)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Используемый движок базы данных
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к файлу базы данных
    }
}

# Валидаторы паролей
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

# Язык и часовой пояс проекта
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'UTC'

# Включение интернационализации и поддержки часовых зон
USE_I18N = True
USE_TZ = True

# Автоматическое поле первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки для статических файлов
STATIC_URL = '/static/'  # URL для статических файлов
STATICFILES_DIRS = [BASE_DIR / 'static',]  # Директории со статическими файлами
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Директория для сбора статических файлов

# Настройки для медиа-файлов
MEDIA_URL = '/media/'  # URL для медиа-файлов
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Директория для хранения медиа-файлов

# Внутренние IP-адреса для отладки
INTERNAL_IPS = ['127.0.0.1',]

# Настройки пользовательской модели пользователя
AUTH_USER_MODEL = 'users.CustomUser'

# Настройки email 
EMAIL_BACKEND = config('EMAIL_BACKEND')               # Используемый бекенд
EMAIL_HOST = config('EMAIL_HOST')                     # SMTP-сервер
EMAIL_PORT = config('EMAIL_PORT', cast=int)           # Порт для SMTP
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)    # Использование SSL
EMAIL_HOST_USER = config('EMAIL_HOST_USER')           # Логин SMTP
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')   # Пароль SMTP
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER                  # Email отправителя
SERVER_EMAIL = EMAIL_HOST_USER                        # Email для системных уведомлений
EMAIL_ADMIN = EMAIL_HOST_USER                         # Email администратора

# Настройки для сессий
CART_SESSION_ID = 'cart'  # Идентификатор корзины в сессии
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Хранилище сессий в базе данных
SESSION_COOKIE_AGE = 86400  # Время жизни сессии (в секундах)
SESSION_SAVE_EVERY_REQUEST = True  # Сохранение сессии при каждом запросе

