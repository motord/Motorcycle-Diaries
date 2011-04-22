# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEFAULT_TIMEZONE = 'Asia/Kuala_Lumpur'
DEBUG = True
PROFILE = False
SECRET_KEY = 'MySecretIsSafeWithNoOne123'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SESSION'

ADD_APP_PREFIX_TO_KIND = True

ADMINS = (
)

TEMPLATE_DIRS = (
)

USE_I18N = True
DEFAULT_LANG = 'en'
FORMS_USE_XHTML = True

INSTALLED_APPS = (
    'kay.auth',
    'blog',
    'piggybank',
    'weatherbug',
)

APP_MOUNT_POINTS = {
    'blog': '/',
}

CONTEXT_PROCESSORS = (
  'kay.context_processors.request',
  'kay.context_processors.url_functions',
  'kay.context_processors.media_url',
)

JINJA2_FILTERS = {
  'nl2br': 'kay.utils.filters.nl2br',
  'date': 'blog.utils.datetimeformat',
}

MIDDLEWARE_CLASSES = (
  'kay.auth.middleware.AuthenticationMiddleware',
)
AUTH_USER_BACKEND = 'kay.auth.backends.googleaccount.GoogleBackend'
AUTH_USER_MODEL = 'kay.auth.models.GoogleUser'
