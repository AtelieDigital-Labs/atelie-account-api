from pathlib import Path
from datetime import timedelta
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


env = environ.Env(DEBUG=(bool, False), ALLOWED_HOSTS=(list, []))

environ.Env.read_env(BASE_DIR / ".env")

ALLOWED_HOSTS=["*"]

SECRET_KEY = env.str("SECRET_KEY")
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
# Permite que o Django entenda o cabeçalho 'X-Forwarded-Proto' enviado pelo Nginx
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Obrigatório a partir do Django 4.0+ para requisições seguras via Proxy
CSRF_TRUSTED_ORIGINS = [
    "https://ateliedigital.dev.br",
]

# 3. Se estiver usando CORS para conectar o React ao Django
# CORS_ALLOWED_ORIGINS = [
#     "https://ateliedigital.dev.br",
# ]
# CORS_ALLOW_CREDENTIALS = True
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # my apps
    "apps.addresses",
    "apps.users",
    "apps.authentication",
    "apps.wallets",
    "apps.audit",
    # other apps
    "rest_framework",
    "rest_framework.authtoken",  # Necessário para tokens básicos
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "drf_spectacular",
    "storages"
]

BACKEND_URL="https://ateliedigital.dev.br"

SITE_ID = 1

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.audit.middleware.AuditContextMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

RABBITMQ_URL = env.str("RABBITMQ_URL")

# django allauth
SOCIALACCOUNT_ADAPTER = "apps.users.adapters.MySocialAccountAdapter"
ACCOUNT_ADAPTER = "apps.users.adapters.AccountAdapter"
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

# dj-rest-auth
ACCOUNT_LOGIN_METHODS = {"email",}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.authentication.authentication.CookieJWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Atelie: Accounts",
    "DESCRIPTION": "Endpoints do micro serviço de Accounts",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_RETURN_EXPIRATION": True,
    "JWT_AUTH_HTTPONLY": True,

    "JWT_AUTH_COOKIE": "access",
    "JWT_AUTH_REFRESH_COOKIE": "refresh",
    "JWT_AUTH_COOKIE_USE_CSRF": True,
    "JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED": False,
    "JWT_AUTH_SECURE": False,  # True em produção com HTTPS
    "JWT_AUTH_SAMESITE": "Lax",
}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env.str("GOOGLE_CLIENT_ID"),
            "secret": env.str("GOOGLE_SECRET"),
            "key": "",
        }
    }
}
GOOGLE_CALLBACK_URL = env("GOOGLE_CALLBACK_URL")
# MinIO 
STORAGES = {
    "default": {
        "BACKEND": "config.storages.CustomMinioStorage", # Sua classe customizada
        "OPTIONS": {
            "access_key": "atelie",
            "secret_key": "atelie123",
            "bucket_name": "accounts",
            "endpoint_url": "http://minio:9000", # Volte para o interno!
            "region_name": "eu-west-1",
            "use_ssl": False,
            "querystring_auth": True, # Mantém assinado
            "file_overwrite": False,
            "addressing_style": "path",
            "signature_version": "s3v4",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MEDIA_URL = "https://ateliedigital.dev.br/media/"
