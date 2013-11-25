from django.shortcuts import render_to_response, RequestContext, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from vcg.admin_management.mail_forms import MailConfigurationForm
from vcg.utilities import admin_login
from vcg.admin_management.models import MailConfiguration

@admin_login
def mail_configuration(request):
    mail_config = MailConfiguration.objects.filter()
    if mail_config:
        mail = mail_config[0]
    else:
        mail = []    
    form = MailConfigurationForm()
    return render_to_response('admin/mail_configuration.html', locals(), context_instance=RequestContext(request))

@admin_login
def mail_configuration_update(request):
    selected_mail_config = MailConfiguration.objects.filter()
    form    = MailConfigurationForm()
    if request.POST:
        if selected_mail_config:
            form = MailConfigurationForm(request.POST, request.FILES, instance = selected_mail_config[0])
        else:
            form = MailConfigurationForm(request.POST, request.FILES)
        if form.is_valid():
            mail = form.save(commit = False)
            mail.created_by = mail.modified_by = request.user
            mail.active = True
            mail.save()
            messages.success(request,(_("Mail Configuration Saved Successfully")),
                                         fail_silently = True)
            return redirect('/admin_management/mail_configuration/')
        else:
            return render_to_response('admin/mail_configuration_update.html', locals(), context_instance=RequestContext(request))
    else:
        if selected_mail_config:
            form = MailConfigurationForm(instance = selected_mail_config[0])
        else:
            form = MailConfigurationForm()   
    return render_to_response('admin/mail_configuration_update.html', locals(), context_instance=RequestContext(request))
