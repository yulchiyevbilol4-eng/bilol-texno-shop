import os
import dj_database_url
from pathlib import Path

# 1. ASOSIY YO'LLAR
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. XAVFSIZLIK VA DEBUG
SECRET_KEY = 'django-insecure-your-secret-key-here'
DEBUG = True # Serverda hamma narsa ishlagach False qiling
ALLOWED_HOSTS = ['*']

# 3. ILOVALAR
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'phones.apps.PhonesConfig',
]

# 4. MIDDLEWARE (WhiteNoise tartibi muhim)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Statik fayllar uchun
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# 5. TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# 6. MA'LUMOTLAR BAZASI (Eng muhim qismi)
# Vercel-dagi Postgres yoki lokal SQLite-ni avtomatik aniqlaydi
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL'),
        conn_max_age=600,
        ssl_require=True if os.environ.get('DATABASE_URL') else False
    )
}

# Agar serverda DATABASE_URL topilmasa (lokal kompyuterda bo'lsangiz)
if not DATABASES.get('default') or not DATABASES['default'].get('ENGINE'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

# 7. PAROL TEKSHIRUVI
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# 8. TIL VA VAQT
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# 9. STATIK VA MEDIA FAYLLAR
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Statik fayllarni serverda siqish va keshlashtirish
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 10. QO'SHIMCHA SOZLAMALAR
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_THOUSAND_SEPARATOR = True
NUMBER_GROUPING = 3

# 11. TELEGRAM BOT
TELEGRAM_BOT_TOKEN = '8142951659:AAFh1kDbysJP7gwvnnkEhC4AbES5cAH86dw'
TELEGRAM_CHAT_ID = '7996293619'