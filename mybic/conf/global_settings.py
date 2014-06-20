"""
Django settings for project_name project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

PROJECT_PATH = BASE_PATH = os.path.join(os.path.dirname(__file__), '../..')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    #core awesome
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #probably needed
    #deprecated
    #'django.contrib.markup',
    'django.contrib.sites',

    #Project apps
    'simple_templates',
    'mybic',

    'south',
    'news',
    'ldap',
)


# Debug

DEBUG = True
TEMPLATE_DEBUG = DEBUG


# Administration

#WSGI_APPLICATION = 'mybic.wsgi.application'

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

#DATABASES = {
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

STATIC_URL = '/static/'

STATICFILES_DIRS = (

)

# Templates

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'mybic.context_processors.static',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



SIMPLE_TEMPLATES_DIR = 'simple_templates'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates')
)

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
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_templates.middleware.SimplePageFallbackMiddleware',
)


# Email

SUPPORT_EMAIL = 'leipzigj@email.chop.edu'
DEFAULT_FROM_EMAIL = 'leipzigj@email.chop.edu'
EMAIL_SUBJECT_PREFIX = '[mybic] '
SEND_BROKEN_LINK_EMAILS = False


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
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
LDAP = {
    'DEBUG': False,
    'PREBINDDN': 'cn=Version Control,ou=AdminUsers,ou=Res,dc=research,'
                 'dc=chop,dc=edu',
    'SEARCHDN': 'dc=chop,dc=edu',
    'SEARCH_FILTER': 'sAMAccountName=%s',
}

# django-registration
REGISTRATION_ACTIVATION_DAYS = 0
REGISTRATION_MODERATION = True
REGISTRATION_BACKENDS = {
    'default': 'pcgc.accounts.backends.DefaultBackend',
}



# CSRF

CSRF_COOKIE_NAME = 'mybic_csrftoken'


# Sessions


# SESSION_COOKIE_AGE = 60 * 20
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_NAME = 'mybic_sessionid'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False


