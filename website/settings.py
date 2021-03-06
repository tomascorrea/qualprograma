# Django settings for website project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'data.db',
        'USER': '',
        'PASSWORD': '',
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

LOG_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'file': { 
            'level': 'DEBUG',
            'class': 'logging.FileHandler', 
            'formatter': 'verbose',        
            'filename': os.path.join(LOG_ROOT, 'qualprograma.log') 
        },
        'robo': {  
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',        
            'filename': os.path.join(LOG_ROOT, 'robos.log') 
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler', 
            'formatter': 'simple',        
        },

    },
    'loggers': {
        'qualprograma': {    
            'handlers': ['file'], 
            'level': 'INFO',     
            'propagate': True,
        },     

        'qualprograma.robos': { 
            'handlers': ['robo', 'console'], 
            'level': 'DEBUG',     
            'propagate': True,
        },        
    }       
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


STATIC_ROOT = '%s/static/' % PROJECT_DIR
STATIC_URL = "/static/"


# Make this unique, and don't share it with anybody.
SECRET_KEY = '=0@0xyamu^ig9qs+o!c@ui@lsv^@yzzw!%^t@%8aon&4e3d4gv'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'website.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'bootstrapform',
    'haystack',
    'core',
    'cinema',
    'endereco',
    'busca',
    'django_nose',
)


HAYSTACK_SITECONF = 'busca.indexes'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = '%s/search_index' % PROJECT_DIR
