"""Django settings

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

import django_stubs_ext
from django.utils.translation import gettext_lazy as _
from environs import Env

# Apply the monkey patches for django-stubs
# https://github.com/typeddjango/django-stubs?tab=readme-ov-file#i-cannot-use-queryset-or-manager-with-type-annotations
django_stubs_ext.monkeypatch()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read environment variables from the environment and a .env file.
env = Env()
env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
# https://docs.djangoproject.com/en/5.1/ref/settings/#debug
DEBUG = env.bool("DEBUG", default=False)

# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key
if DEBUG:
    SECRET_KEY = env.str("SECRET_KEY", default="A_NOT_SO_SAVE_DEFAULT_KEY")
else:
    SECRET_KEY = env.str("SECRET_KEY", "")

# A list of strings representing the host/domain names that this Django site can serve.
# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# A list of IP addresses that are allowed to access the django debug toolbar.
# https://docs.djangoproject.com/en/5.1/ref/settings/#internal-ips
INTERNAL_IPS = env.list("INTERNAL_IPS", default=[])

# A list of trusted origins for unsafe requests (e.g. POST).
# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Application definition
# https://docs.djangoproject.com/en/5.1/ref/settings/#installed-apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

# Third-party apps
INSTALLED_APPS += [
    "django_browser_reload",
    "django_htmx",
    "django_tailwind_cli",
    "django_extensions",
    "unique_user_email",
]

# Our apps
INSTALLED_APPS += ["{{ cookiecutter.package_name }}"]

# Middleware definitions
# https://docs.djangoproject.com/en/5.1/topics/http/middleware/
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

# A string representing the full Python import path to your root URLconf.
# https://docs.djangoproject.com/en/5.1/ref/settings/#root-urlconf
ROOT_URLCONF = "{{ cookiecutter.package_name }}.urls"

# A list containing the settings for all template engines to be used with Django.
# https://docs.djangoproject.com/en/5.1/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.csrf",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
            ],
            "builtins": [
                # "django.contrib.humanize.templatetags.humanize",
                "django.templatetags.i18n",
                # "django.templatetags.l10n",
                "django.templatetags.static",
                # "django.templatetags.tz"
                "heroicons.templatetags.heroicons",
            ],
        },
    },
]

# The full Python path of the WSGI application object that Django`s built-in servers
# (e.g. runserver) will use.
# https://docs.djangoproject.com/en/5.1/ref/settings/#wsgi-application
WSGI_APPLICATION = "{{ cookiecutter.package_name }}.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {"default": env.dj_db_url("DATABASE_URL", default="sqlite:///db.sqlite3")}

if DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
    DATABASES["default"].setdefault("OPTIONS", {})["init_command"] = (
        "PRAGMA foreign_keys=ON;"
        "PRAGMA journal_mode = WAL;"
        "PRAGMA synchronous = NORMAL;"
        "PRAGMA busy_timeout = 5000;"
        "PRAGMA temp_store = MEMORY;"
        "PRAGMA mmap_size = 134217728;"
        "PRAGMA journal_size_limit = 67108864;"
        "PRAGMA cache_size = 2000;"
    )
    DATABASES["default"]["OPTIONS"]["transaction_mode"] = "IMMEDIATE"


# Authentication backends
# https://docs.djangoproject.com/en/5.1/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "unique_user_email.backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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

# Password hashers
# https://docs.djangoproject.com/en/dev/topics/auth/passwords/
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="en")
LANGUAGES = [
    ("en", _("English")),
    ("de", _("German")),
]
TIME_ZONE = env.str("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# Static files (SCSS, CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# https://docs.djangoproject.com/en/5.1/ref/settings/#static-files
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
STATICFILES_DIRS = (str(BASE_DIR / "assets"),)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# User uploaded static files
# https://docs.djangoproject.com/en/5.1/ref/settings/#media-url
# https://docs.djangoproject.com/en/5.1/ref/settings/#media-root
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Email backend
# https://docs.djangoproject.com/en/5.1/ref/settings/#email-backend
# https://docs.djangoproject.com/en/5.1/topics/email/
EMAIL_CONFIG = env.dj_email_url("EMAIL_URL", default="console:")
vars().update(EMAIL_CONFIG)

# Caches
# https://docs.djangoproject.com/en/5.1/ref/settings/#caches
CACHES = {"default": env.dj_cache_url("CACHE_URL", default="locmem://")}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-tailwind-cli settings
# https://django-tailwind-cli.andrich.me/settings/
TAILWIND_CLI_PATH = env.str("TAILWIND_CLI_PATH", default="~/.local/bin")
