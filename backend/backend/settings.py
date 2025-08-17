from pathlib import Path
from decouple import config  # เพิ่มการจัดการตัวแปรจาก .env
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# เพิ่ม path สำหรับ apps
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-i2_@o)46eseo+vhapcm+^0!ye1x9e&8^4q&glrn_atal*fkske')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',
    'apps.users.apps.UsersConfig',  # ใช้ AppConfig เพื่อกำหนด custom user
    'apps.leave.apps.LeaveConfig',
    'apps.work_from_outside.apps.WorkFromOutsideConfig',
    'apps.holiday.apps.HolidayConfig',
    'apps.attendance.apps.AttendanceConfig',
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

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # เพิ่มเพื่อรองรับ template
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

WSGI_APPLICATION = 'backend.wsgi.application'

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='devdb'),
        'USER': config('DB_USER', default='devuser'),
        'PASSWORD': config('DB_PASSWORD', default='devpass'),
        'HOST': config('DB_HOST', default='mariadb'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'apps.users.validators.CustomMinimumLengthValidator',  # ใช้ custom validator
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'apps.users.validators.ComplexPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'th'  # เปลี่ยนเป็นภาษาไทย
TIME_ZONE = 'Asia/Bangkok'  # เปลี่ยนเป็นโซนเวลาไทย
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static',]  # ลบชั่วคราวเพื่อป้องกัน warning จนกว่าจะสร้างโฟลเดอร์
STATICFILES_DIRS = []  # ปิด warning ชั่วคราว
STATIC_ROOT = BASE_DIR / 'staticfiles'  # สำหรับ collectstatic

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery Settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Bangkok'

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

# NEW: Cron Job Reset สิทธิ์ทุกวันที่ 1 มกราคม
CRONJOBS = [
    ('0 0 1 1 *', 'leaves.cron.reset_leave_quota')
]

FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = 'http://localhost:8000'
DEFAULT_FROM_EMAIL = "no-reply@yourdomain.com"
