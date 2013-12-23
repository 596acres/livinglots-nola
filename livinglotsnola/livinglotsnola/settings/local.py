from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'admin@example.com'),
)

MANAGERS = ADMINS

FACILITATORS = {
    'global': ['facilitator@example.com',],
}

TIME_ZONE = 'America/New_York'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, '../logs', 'django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['log_file',],
        'level': 'DEBUG',
    },
}


#
# debug toolbar settings
#

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES += (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'django_pdb.middleware.PdbMiddleware',
)

INSTALLED_APPS += (
    #'debug_toolbar',
    #'django_pdb',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

NOLADATA_TREASURY_PARCELS_GEOPINS = '/home/eric/Documents/596/nola_vacancy_working/probably_vacant_geopin.csv'
