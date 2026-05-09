import os
from pathlib import Path

# Loyihaning asosiy yo'li
BASE_DIR = Path(__file__).resolve().parent.parent

# Xavfsizlik kaliti (Ishlab chiqish jarayoni uchun)
SECRET_KEY = 'django-insecure-your-secret-key-here'

# Debug rejimini yoqish (Xatolarni ko'rish uchun)
DEBUG = True

ALLOWED_HOSTS = ['*'] # Barcha hostlarga ruxsat berish

# O'rnatilgan ilovalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Sizning ilovangiz
    'phones.apps.PhonesConfig', # Ilovani to'liq nomi bilan ko'rsatish tavsiya etiladi
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'core.urls' # Loyihangiz papkasi nomi 'core' bo'lsa shunday qoladi

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',          # Asosiy papkadagi templates
            BASE_DIR / 'phones' / 'templates' # Phones ichidagi templates
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

# Ma'lumotlar bazasi (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Parol tekshiruvi
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Til va vaqt sozlamalari
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# --- STATIK VA MEDIA FAYLLAR ---

# CSS, JavaScript va rasmlar uchun
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Serverda statik fayllarni yig'ish uchun
STATICFILES_DIRS = [BASE_DIR / 'static'] # Ish jarayonidagi statik fayllar joyi

# MEDIA FAYLLAR (Telefon rasmlari uchun!)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py oxiriga qo'shing yoki borini tekshiring
USE_THOUSAND_SEPARATOR = True
USE_L10N = True
# Tiyinlarni (verguldan keyingi qismni) butkul o'chirish uchun:
DECIMAL_SEPARATOR = ','
NUMBER_GROUPING = 3
# --- TELEGRAM BOT SOZLAMALARI ---
# BotFather'dan olingan token (tirnoq ichiga yozing)
TELEGRAM_BOT_TOKEN = '8142951659:AAFh1kDbysJP7gwvnnkEhC4AbES5cAH86dw' 

# Xabar borishi kerak bo'lgan guruh yoki shaxsiy ID (faqat raqamlar)
TELEGRAM_CHAT_ID = '7996293619'