from django.db import models
from django.contrib.auth.models import User

class Audit(models.Model):
    created_by  = models.ForeignKey(User, related_name='created_%(class)s_set', null=True, blank=True, verbose_name = "Created By")
    modified_by = models.ForeignKey(User, related_name='updated_%(class)s_set', null=True, blank=True, verbose_name = "Modified By")
    created_at  = models.DateTimeField(auto_now_add = True, verbose_name = "Created At",        null=True, blank=True)
    modified_at = models.DateTimeField(auto_now = True,     verbose_name = "Last Modified At",  null=True, blank=True)
  
    def send_notification_mail(self):
        return False; 

    def get_view_permission(self):
        return 'view_%s' % self.object_name.lower()

    class Meta:
        abstract = True
        
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

#*****  AUTOMATIC SUPER USER CREATION *******************

# From http://stackoverflow.com/questions/1466827/ --

# Create our own test user automatically.

def create_testuser(app, created_models, verbosity, **kwargs):
#    if not settings.DEBUG:
#        return
    try:
        auth_models.User.objects.using('default').get(username=settings.SUPER_USER_USERNAME)
    except auth_models.User.DoesNotExist:
        print '*' * 80
        print 'Creating Super User -- Username: %s, Password: %s' % (settings.SUPER_USER_USERNAME, settings.SUPER_USER_PASSWORD)
        print '*' * 80
        assert auth_models.User.objects.db_manager('default').create_superuser(settings.SUPER_USER_USERNAME, settings.SUPER_USER_EMAIL, settings.SUPER_USER_PASSWORD)
    else:
        print 'Given user already exists.'


# Prevent interactive question about wanting a superuser created.  (This code
# has to go in this otherwise empty "models" module so that it gets processed by
# the "syncdb" command during database creation.)

if settings.AUTO_SUPER_USER_CREATION:
    signals.post_syncdb.disconnect( create_superuser, sender=auth_models, dispatch_uid='django.contrib.auth.management.create_superuser')
    signals.post_syncdb.connect(    create_testuser,  sender=auth_models, dispatch_uid='util.models.create_testuser')

from django.views.generic.base import TemplateView

class TextPlainView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TextPlainView, self).render_to_response(context, content_type='text/plain', **kwargs)