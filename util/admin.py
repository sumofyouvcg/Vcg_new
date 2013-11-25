from datetime import datetime

from django.db import models
from django.core.mail import mail_managers
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.contrib import admin

from reversion.admin import  VersionAdmin #@UnresolvedImport

def update_status(self, request, queryset, status, model_singular, model_plural):
    update_list = queryset.exclude(status__exact = status)

    for object in update_list:
        if object.send_notification_mail():
            subject = "%s : '%s'  has been updated [Changed Status]" % (str(ContentType.objects.get_for_model(object)).title(), force_unicode(object))
            body = " %s by '%s' at %s " % (subject, request.user, datetime.now())
            mail_managers(subject, body, fail_silently = False)

    rows_updated = update_list.update(status = status, modified_at = datetime.now(), modified_by = request.user)

    if rows_updated == 1:
        message_bit = "1 %s  was " % (model_singular)
    elif rows_updated > 1:
        message_bit =  "%s %s were" % (rows_updated, model_plural) 
    else:
        message_bit = "No %s was" % (model_singular)
        
    status_message = "%s successfully marked as %s." % (message_bit, status)        
    self.message_user(request, status_message)

def save_model(self, request, obj, form, change):
    instance = form.save(commit = False)
    if not instance.created_at and not instance.modified_at:
        instance.created_by = request.user
    instance.modified_by = request.user
    instance.save()        
    form.save_m2m()
    return instance
    
def log_common(self, request, object, message, action_flag): 
    LogEntry.objects.log_action(
            user_id         = request.user.pk,
            content_type_id = ContentType.objects.get_for_model(object).pk,
            object_id       = object.pk,
            object_repr     = force_unicode(object),
            action_flag     = action_flag,
            change_message  = message
        )
    
    if object.send_notification_mail():
        if action_flag == ADDITION:
            action_message = ' created'
        if action_flag == CHANGE:
            if message.startswith('No'):
                return
            else:
                action_message = ' updated [%s]' % (message)
        if action_flag == DELETION:
            action_message = ' deleted'
                
        subject = "%s : '%s'  has been %s " % (str(ContentType.objects.get_for_model(object)).title(), force_unicode(object), action_message)
        body = " %s by '%s' at %s " % (subject, request.user, datetime.now())
        mail_managers(subject, body, fail_silently = False)

class BaseAuditAdmin(admin.ModelAdmin):   
    list_display    = ('created_by', 'modified_by', 'created_at', 'modified_at',)
    exclude = ('created_by', 'modified_by',)
    
    save_on_top = True
    
    def save_model(self, request, obj, form, change):
        save_model(self, request, obj, form, change)
    
    def log_addition(self, request, object):
        log_common(self, request, object, "", ADDITION)

    def log_change(self, request, object, message):
        log_common(self, request, object, message, CHANGE)

    def log_deletion(self, request, object, object_repr):
        log_common(self, request, object, "", DELETION)
    
    def __init__(self, *args, **kwargs):
        super(BaseAuditAdmin, self).__init__(*args, **kwargs)
        #self.form.label_suffix = 'some suffix here'

class AuditAdmin(BaseAuditAdmin, VersionAdmin):
    exclude = ('created_by', 'modified_by',)    
    
class AuditInlineAdmin(admin.TabularInline):
    exclude = ('created_by', 'modified_by',)
    extra = 0

    def save_model(self, request, obj, form, change):
        save_model(self, request, obj, form, change)

    def log_addition(self, request, object):
        log_common(self, request, object, "", ADDITION)

    def log_change(self, request, object, message):
        log_common(self, request, object, message, CHANGE)

    def log_deletion(self, request, object, object_repr):
        log_common(self, request, object, "", DELETION)
        
class AuditAdminWithNoLinks(AuditAdmin):
        
    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        self.inline_instances = []
        for inline_class in self.inlines:
            inline_instance = inline_class(self.model, self.admin_site)
            self.inline_instances.append(inline_instance)
        if 'action_checkbox' not in self.list_display and self.actions is not None:
            self.list_display = ['action_checkbox'] +  list(self.list_display)
        if not self.list_display_links:
            for name in self.list_display:
                if name != 'action_checkbox':
                    break
        super(admin.ModelAdmin, self).__init__()