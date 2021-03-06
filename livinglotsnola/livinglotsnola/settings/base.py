from collections import OrderedDict
import os
from os.path import abspath, dirname

from django.core.exceptions import ImproperlyConfigured


ENV_VARIABLE_PREFIX = 'LLNOLA'

def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    if not ENV_VARIABLE_PREFIX:
        raise ImproperlyConfigured('Set ENV_VARIABLE_PREFIX')
    try:
        return os.environ[ENV_VARIABLE_PREFIX + '_' + var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)


DATABASES = {
    'default': {
        # > createdb -T template_postgis livinglotsnola
        # > psql
        # # create user livinglotsnola with password 'password';
        # # grant all privileges on database livinglotsnola to
        # livinglotsnola;
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
    }
}

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
)

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = 'America/New_York'

PROJECT_ROOT = os.path.join(abspath(dirname(__file__)), '..', '..')

DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = get_env_variable('SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'honeypot.middleware.HoneypotMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',

    'feincms.context_processors.add_page_if_missing',
)

ROOT_URLCONF = 'livinglotsnola.urls'

WSGI_APPLICATION = 'livinglotsnola.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    #
    # django contrib
    #
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',

    #
    # third-party
    #
    'actstream',
    'admin_enhancer',
    'compressor',
    'contact_form',
    'django_monitor',
    'djangojs',
    'elephantblog',
    'feincms',
    'feincms.module.medialibrary',
    'feincms.module.page',
    'flatblocks',
    'honeypot',
    'imagekit',
    'inplace',
    'inplace.boundaries',
    'jsonfield',
    'mptt',
    'reversion',
    'reversion_compare',
    'south',
    'widget_tweaks',

    #
    # first-party, project-generic
    #
    'external_data_sync',
    'inplace_activity_stream',
    'pagepermissions',

    # Living Lots
    'livinglots_lots',
    'livinglots_notify',
    'livinglots_organize',
    'livinglots_owners',
    'livinglots_pathways',
    'livinglots_steward',
    'livinglots_usercontent.files',
    'livinglots_usercontent.notes',
    'livinglots_usercontent.photos',

    'noladata',
    'noladata.addresses',
    'noladata.assessor',
    'noladata.buildings',
    'noladata.codeenforcement',
    'noladata.councildistricts',
    'noladata.datasync',
    'noladata.habitat',
    'noladata.hano',
    'noladata.neighborhoodgroups',
    'noladata.nora',
    'noladata.parcels',
    'noladata.treasury',
    'noladata.zipcodes',
    'noladata.zoning',

    #
    # first-party, project-specific
    #
    'activity_stream',
    'blog',
    'cms',
    'contact',
    'groundtruth',
    'lots',
    'organize',
    'owners',
    'pathways',
    'steward',
    'usercontent',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

PLACES_MAPBOX_ID = 'livinglotsnola.i29k40f5'

SOUTH_TESTS_MIGRATE = False

RECAPTCHA_PRIVATE_KEY = get_env_variable('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = get_env_variable('RECAPTCHA_PUBLIC_KEY')

ORGANIZE_PARTICIPANT_SALT = get_env_variable('ORGANIZE_PARTICIPANT_SALT')

ACTSTREAM_SETTINGS = {
    'MANAGER': 'inplace_activity_stream.managers.PlaceActionManager',
    'MODELS': (
        'auth.user',
        'files.file',
        'lots.lot',
        'notes.note',
        'organize.organizer',
        'photos.photo',
    ),
    'USE_JSONFIELD': True,
}
ACTIVITY_STREAM_DEFAULT_ACTOR_PK = get_env_variable('ACTSTREAM_DEFAULT_ACTOR_PK')

FACILITATORS = {
    'global': [],
}

EMAIL_SUBJECT_PREFIX = '[Living Lots NOLA] '

MAILREADER_REPLY_PREFIX = 'Reply with text above this line to post a public note.'
MAILREADER_IGNORE_FROM = []
MAILREADER_HOST = get_env_variable('MAILREADER_HOST')
MAILREADER_HOST_USER = get_env_variable('MAILREADER_HOST_USER')
MAILREADER_HOST_PASSWORD = get_env_variable('MAILREADER_HOST_PASSWORD')

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_richtext.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + 'bower_components/tinymce/js/tinymce/tinymce.js',
}

def elephantblog_entry_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('elephantblog_entry_detail', 'elephantblog.urls',
                       kwargs={
                           'year': self.published_on.strftime('%Y'),
                           'month': self.published_on.strftime('%m'),
                           'day': self.published_on.strftime('%d'),
                           'slug': self.slug,
                       })


def elephantblog_categorytranslation_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('elephantblog_category_detail', 'elephantblog.urls',
                       kwargs={ 'slug': self.slug, })


ABSOLUTE_URL_OVERRIDES = {
    'elephantblog.entry': elephantblog_entry_url_app,
    'elephantblog.categorytranslation': elephantblog_categorytranslation_url_app,
}

HONEYPOT_FIELD_NAME = 'homepage_url'
HONEYPOT_VALUE = 'http://example.com/'

ADMIN_TOOLS_INDEX_DASHBOARD = 'livinglotsnola.admindashboard.LivingLotsDashboard'

LIVING_LOTS = {
    'MODELS': {
        'lot': 'lots.Lot',
        'lotgroup': 'lots.LotGroup',
        'organizer': 'organize.Organizer',
        'owner': 'owners.Owner',
        'pathway': 'pathways.Pathway',
    },
}

CONTACT_FORM_REASONS = OrderedDict([
    ('The lot I want permission to use is not on Living Lots NOLA.', ['info@livinglotsnola.org',]),
    ('I want to share my NOLA land access story.', ['info@livinglotsnola.org',]),
    ('I want to donate my land so that it can be protected open space.', ['Bridget.Kelly@LandTrustforLouisiana.org',]),
    ('I want to loan or lease my land for a temporary project.', ['info@livinglotsnola.org',]),
    ('I want to invite Living Lots admins to an event.', ['info@livinglotsnola.org',]),
    ('I want to reach 596 Acres, the team that made this site.', ['paula@596acres.org',]),
    ('I have a press inquiry.', ['info@livinglotsnola.org',]),
])

SOUTH_MIGRATION_MODULES = {
    'page': 'cms.migrate.page',
    'medialibrary': 'cms.migrate.medialibrary',
}

NOLADATA_TREASURY_BASE_TAX_URL = 'http://services.nola.gov/service.aspx?load=treasury&Type=1&TaxBill='
NOLADATA_TREASURY_UA = ('Mozilla/5.0 (Windows NT 6.2; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/32.0.1667.0 Safari/537.36')
