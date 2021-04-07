import os
import django_heroku
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."
DEBUG = True
ALLOWED_HOSTS = ['*']
CRISPY_TEMPLATE_PACK = 'bootstrap4'
IMPORT_EXPORT_USE_TRANSACTIONS = True
INSTALLED_APPS = [
    'simpleui', 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
    "django_filters",
    'crispy_forms',
    "hello",
    'import_export',
    'simple_history'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware"
]

ROOT_URLCONF = "gettingstarted.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


if os.getenv('GAE_APPLICATION', None):
    # Running on AppEngine, connect to CloudSQL:
    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/ml-vps:us-central1:techstaff-db',
            'USER': 'techstaff',
            'PASSWORD': 'nYlenIldpqKdneo8Ndqjkc28J',
            'NAME': 'techstaff'
        }
    }

else:
    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '35.192.209.96',
            'USER': 'techstaff',
            'PASSWORD': 'nYlenIldpqKdneo8Ndqjkc28J',
            'NAME': 'techstaff'
        }
    }
    """ DATABASES = {

        'default': {

            'ENGINE': 'django.db.backends.postgresql_psycopg2',

            'NAME': 'dcor75c08ep5v',

            'USER': 'shvavxjzucmbod',

            'PASSWORD': '1bed704e7a1ba22d18a2d1ca3b3965d9d8b59aa38219ed2115609b40a46a8e6a',

            'HOST': 'ec2-34-192-106-123.compute-1.amazonaws.com',

            'PORT': '5432',

        }

    } """

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = 'static'
django_heroku.settings(locals())
SIMPLEUI_LOGO = 'https://www.assets.cms.vt.edu/images/maroon-shield.png'
SIMPLEUI_ANALYSIS = False
SIMPLEUI_LOGIN_PARTICLES = False
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ICON = {
    'Facultys': 'fas fa-address-card',
    'Devices': 'fab fa-apple',
    'Network interfaces': 'fas fa-at',
    'Buildings': 'fas fa-building',
    'User devices': 'fas fa-check-circle'
}
