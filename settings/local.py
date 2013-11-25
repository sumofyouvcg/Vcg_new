import dj_database_url

DATABASES = {'default': dj_database_url.config(default='mysql://root:root@localhost/vcg')}

DEBUG = True
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'vcg',                      # Or path to database file if using sqlite3.
#        'USER': 'root',                      # Not used with sqlite3.
#        'PASSWORD': 'root',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}
#SESSION_COOKIE_DOMAIN = 'localhost'
#
#IONFACE_DOMAIN_NAME = 'localhost:8000'
#
#IMAGE_FOLDER_PATH = 'localhost:8000/site_media/mugshots/'
#
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVER_DOMAIN_URL = 'localhost:8000'

#LANGUAGE_CODE = 'nl-NL'