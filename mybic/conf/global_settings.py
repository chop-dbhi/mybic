"""
Django settings for project_name project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from chopauth.settings import *

PROJECT_PATH = BASE_PATH = os.path.join(os.path.dirname(__file__), '../..')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['mybic.chop.edu', 'localhost', '10.30.9.53']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'mybic',
    'mybic.labs',
    'south',
    'news',
    'ldap',

    'chopauth',

    'haystack',

    'tracking'
)


# Administration

# WSGI_APPLICATION = 'mybic.wsgi.application'

# Admins receive any error messages by email if DEBUG is False
ADMINS = (
    ('Jeremy Leipzig', 'leipzigj@email.chop.edu'),
)

# Managers receive broken link emails if SEND_BROKEN_LINK_EMAILS is True
MANAGERS = ADMINS

# List of IP addresses which will show debug comments
INTERNAL_IPS = ('127.0.0.1', '::1')


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_PATH, 'mybic.db'),
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_PATH, '_site/media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_PATH, '_site/static')

PROTECTED_ROOT = os.path.join(BASE_PATH, '_site/protected')

APP_PATH = os.path.join(PROJECT_PATH, 'mybic')

TEMPLATE_ROOT = os.path.join(APP_PATH, 'labs', 'templates')

STATIC_URL = '/static/'

PROTECTED_URL = '/slink/'

# '.txt'
EXTRACTION_SUFFIXES = ('.html', '.md', '.pdf')

# Templates

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'mybic.context_processors.static',
    'mybic.context_processors.development',
    'mybic.context_processors.version',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

# List of finder classes that know how to find static files in
# various locations.
#STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
#)



# URLs

ROOT_URLCONF = 'mybic.conf.urls'

# FORCE_SCRIPT_NAME overrides the interpreted 'SCRIPT_NAME' provided by the
# web server. since the URLs below are used for various purposes outside of
# the WSGI application (static and media files), these need to be updated to
# reflect this discrepancy.
FORCE_SCRIPT_NAME = ''

IGNORABLE_404_PATHS = (
    r'robots.txt$',
    r'favicon.ico$',
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
#django sets this to /accounts/profile
LOGIN_REDIRECT_URL = '/dashboard/'

SITEAUTH_ACCESS_ORDER = 'allow/deny'

SITEAUTH_ALLOW_URLS = (
    r'^$',
    r'^favicon\.ico$',
    r'^documentation/',
    r'^(static|login|logout|denied|eula|support)/',
    r'^concerns/$',
    r'^password/reset/',
    r'^(register|verify)/',
)


# The primary key of the ``Site`` object for the Sites Framework
SITE_ID = 1



# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'siteauth.middleware.SiteAuthenticationMiddleware'
)


# Email

# SUPPORT_EMAIL = '"myBiC"<mybic@mybic.chop.edu>'
# DEFAULT_FROM_EMAIL = '"myBiC"<mybic@mybic.chop.edu>'
# EMAIL_SUBJECT_PREFIX = '[mybic] '
#the middleware does this methinks
#SEND_BROKEN_LINK_EMAILS = True
# SERVER_EMAIL = '"myBiC"<nobody@mybic.chop.edu>'

DEFAULT_FROM_EMAIL = 'webmaster@localhost'  # or webmaster@servername
SERVER_EMAIL = 'root@localhost'  # or 'root@servername'
EMAIL_HOST = 'localhost'  # or servername
EMAIL_HOST_USER = ''  # or 'user@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 25  #587
EMAIL_USE_TLS = True


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'mail_owner': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'mybic.utils.log.ProjectEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stderr
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'protected_file': {
            'handlers': ['mail_owner'],
            'level': 'ERROR',
            'propagate': True,
        },

    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
}


# Caches

# For production environments, the memcached backend is highly recommended
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique',
        'KEY_PREFIX': 'mybic',
        'VERSION': 1,
    }
}



#
# AUTHENTICATION
#

# Two additional auth backends for email-based (rather than username)
# and LDAP-based authentication. To use the LDAP authentication, the
# rematining LDAP settings (see below) must be defined.
#AUTHENTICATION_BACKENDS = (
#    'pcgc.core.backends.EmailBackend',
#    'pcgc.core.backends.LdapBackend',
#    'django.contrib.auth.backends.ModelBackend',
#)

# LDAP Authentication Backend -- LDAP['PREBINDPW'] and LDAP['SERVER_URI']
# must be defined in local_settings.py since they are sensitive settings.

AUTHENTICATION_BACKENDS = (
    'chopauth.backends.LdapBackend',
    'django.contrib.auth.backends.ModelBackend',
)

REGISTRATION_BACKENDS = {
    'default': 'chopauth.regbackends.DefaultBackend',
}

LDAP = {
    'DEBUG': False,
    'PREBINDDN': 'cn=Version Control,ou=AdminUsers,ou=Res,dc=research,dc=chop,dc=edu',
    'SEARCHDN': 'dc=chop,dc=edu',
    'SEARCH_FILTER': 'sAMAccountName=%s',
}


# django-registration
REGISTRATION_ACTIVATION_DAYS = 0
REGISTRATION_MODERATION = True
REGISTRATION_BACKENDS = {
    'default': 'chopauth.regbackends.DefaultBackend',
}



# CSRF

CSRF_COOKIE_NAME = 'mybic_csrftoken'


# Sessions


SESSION_COOKIE_AGE = 60 * 20
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_NAME = 'mybic_sessionid'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False



#Haystack
# 'elasticsearch': {
#     'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#     'URL': 'http://127.0.0.1:9200/',
#     'INDEX_NAME': 'haystack',
# },
# 'solr': {
#     'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#     'URL': 'http://127.0.0.1:8983/solr',
#     'BATCH_SIZE': 1,
# }


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'BATCH_SIZE': 5,
        'EXCLUDED_INDEXES': [
            'news.search_indexes.ArticleIndex',
        ],
        'TIMEOUT': 60 * 5,
    }
}


# tracking
TRACK_AJAX_REQUESTS = False
TRACK_ANONYMOUS_USERS = False

TRACK_PAGEVIEWS = True

TRACK_IGNORE_URLS = r'^(favicon\.ico|robots\.txt)$',

TRACK_IGNORE_STATUS_CODES = []

TRACK_USING_GEOIP = False

TRACK_REFERER = False

TRACK_QUERY_STRING = True

PAGEVIEW_LIMIT = 100
