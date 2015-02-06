import os
from django.conf import settings
from mybic import __version__


def static(request):
    "Shorthand static URLs. In debug mode, the JavaScript is not minified."
    static_url = settings.STATIC_URL
    prefix = 'src' if settings.DEBUG else 'min'
    return {
        'CSS_URL': os.path.join(static_url, 'stylesheets/css'),
        'IMAGES_URL': os.path.join(static_url, 'images'),
        'JAVASCRIPT_URL': os.path.join(static_url, 'scripts/javascript', prefix),
    }


def version(request):
    """Provides an APP_VERSION variable"""
    return {
        'APP_VERSION': "{0}".format(__version__)
    }


def development(request):
    """Development warning for indicating which site you are on"""
    if settings.DEVELOPMENT:
        return {
            'DEVELOPMENT': 'DEVELOP BRANCH'
        }
    else:
        return {
            'DEVELOPMENT': ''
        }
