from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== Entorno (.env) =====
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ===== Seguridad / Debug / Hosts =====
SECRET_KEY = env("SECRET_KEY", default="dev-insecure-key-change-me")
DEBUG = env("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# ===== Internacionalización =====
LANGUAGE_CODE = env("LANGUAGE_CODE", default="es-ar")
TIME_ZONE = env("TIME_ZONE", default="America/Argentina/Buenos_Aires")
USE_I18N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'asistencias',
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

ROOT_URLCONF = 'asistencia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'asistencia.wsgi.application'

# ===== Base de datos (SQLite por defecto, MySQL opcional vía .env) =====
DB_ENGINE = env("DB_ENGINE", default="sqlite").lower()
if DB_ENGINE == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST', default='127.0.0.1'),
            'PORT': env('DB_PORT', default='3306'),
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / env('DB_NAME', default='db.sqlite3'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


AUTH_USER_MODEL = 'asistencias.User'

# Nombre institucional para exportes/reportes
INSTITUTO_NOMBRE = "Instituto CENT40 - Campus Virtual Río Negro"

# === Password reset ===
# Link de restablecimiento válido por 24 horas (en segundos)
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24

# === Email: dev por consola / prod por SMTP vía .env ===
# En DEBUG=True se usa consola; en producción se toman valores de .env
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'no-reply@siga.local'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST', default='')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)  # usar uno u otro, no ambos
    EMAIL_TIMEOUT = env.int('EMAIL_TIMEOUT', default=30)
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='no-reply@tu-dominio.com')
    SERVER_EMAIL = env('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)  # para errores de Django

# (Opcional) Dominio/CSRF si usás password reset detrás de un dominio público
# CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Mantener sesión por 7 días si "recordarme" está activo
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 días
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
