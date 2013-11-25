# Django settings for vcg project.

import os, dj_database_url

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__).decode('utf-8')).replace('/settings','/').replace('\\settings','\\') # For windows

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='mysql://pydan_vcg:root@localhost/pydan_vcg')}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'pydan_vcg',                      # Or path to database file if using sqlite3.
#        'USER': 'pydan_vcg',                      # Not used with sqlite3.
#        'PASSWORD': 'root',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(CURRENT_PATH, 'uploads').replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(CURRENT_PATH, 'media').replace('\\','/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3r@8qv1wpke4jvz&!$-(i!#bckv40g_2+vu&mfdzl*uzmf5r09'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'vcg.config.custom_middleware.SessionBasedLocaleMiddleware'
#    'django-session-idle-timeout.middleware.SessionIdleTimeout',
)

ROOT_URLCONF = 'vcg.urls'

TEMPLATE_DIRS = (
                 os.path.join(CURRENT_PATH, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',

    # django 1.2 only
    'django.contrib.messages.context_processors.messages',

    # required by django-admin-tools
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    # Modules
    'util',
    'admin_management',
    'company_management',
    'client_management',
    'caregiver_management',
    'ckeditor',
    
    # 3rd Party Apps
    'request',
    'reversion',
    'django_countries',
#    'django-session-idle-timeout',
)

#STATIC_DOC_ROOT = os.path.join(CURRENT_PATH, 'media').replace('\\','/')

if not os.path.isdir(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
CKEDITOR_UPLOAD_PATH = MEDIA_ROOT

ADMIN_TOOLS_INDEX_DASHBOARD = 'vcg.util.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_MENU = 'vcg.util.menu.CustomMenu'

AUTO_SUPER_USER_CREATION    = True
SUPER_USER_USERNAME         = 's'         
SUPER_USER_PASSWORD         = 's'
SUPER_USER_EMAIL            = 'test@pydan.com'

LOGIN_URL = '/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#SESSION_IDLE_TIMEOUT = 1800

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_HOST              = 'smtp.gmail.com'
EMAIL_PORT              = 587 # 465 for TLS
EMAIL_HOST_USER         = 'notifications@pydan.com'
EMAIL_HOST_PASSWORD     = 'redhat77'
EMAIL_SUBJECT_PREFIX    = '[VCG] '
EMAIL_USE_TLS           = True
DEFAULT_FROM_EMAIL      = EMAIL_HOST_USER
SERVER_EMAIL            = EMAIL_HOST_USER

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SERVER_DOMAIN_URL = 'pmp.sumofyou.in'