from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

DEBUG = True

ALLOWED_HOSTS = [
    "*",
    ".vercel.app",
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    "news",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Serverless platforms (incl. Vercel) have a read-only project dir; /tmp is writable.
# Also avoid DB-backed sessions on serverless.
_is_serverless = any(
    os.environ.get(k)
    for k in [
        "VERCEL",
        "VERCEL_REGION",
        "VERCEL_ENV",
        "AWS_LAMBDA_FUNCTION_NAME",
        "AWS_EXECUTION_ENV",
    ]
)
if _is_serverless or str(BASE_DIR).startswith("/var/task"):
    DATABASES["default"]["NAME"] = "/tmp/db.sqlite3"
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://*.vercel.app",
    "https://predict-fake-news-python-sklearn.vercel.app",
    "https://fake-new-fe-react-vite.vercel.app",
]