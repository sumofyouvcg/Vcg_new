from django.shortcuts import render_to_response, HttpResponseRedirect, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from vcg.admin_management.client_forms import ClientForm
from vcg.admin_management.models import Client
from vcg.utilities import client_login

@client_login
def client_home(request, domain_name = None, comp_id = None):
    return redirect(reverse('client_task_list', kwargs={'domain_name': domain_name}))
#    return render_to_response('client/client_home.html', locals(), context_instance=RequestContext(request))

@client_login
def my_profile(request, domain_name = None):
    try:
        try_client = Client.objects.get(client_number = request.user.username)
        selected_client = get_object_or_404(Client, client_number = request.user.username)
        old_email = selected_client.email
        if request.POST:
            form = ClientForm(request.POST, request.FILES,instance = selected_client)
            if form.is_valid():
                client = form.save(commit = False)
                client.created_by = client.modified_by = request.user
                if not form.files:
                    client.client_image = ''
                client.save()
                User.objects.filter(username = client.client_number).update(first_name = client.name)
                if old_email != client.email:
                    User.objects.filter(email = old_email).update(username = client.client_number, email = client.email)
                messages.success(request,(_("Your Profile Edited Successfully")),fail_silently = True)
                return redirect(reverse('client_task_list', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('client/my_profile.html', locals(), context_instance=RequestContext(request))
        else:
            form = ClientForm(instance = selected_client)
        return render_to_response('client/my_profile.html', locals(), context_instance=RequestContext(request))
    except Client.DoesNotExist:
        messages.success(request,(_('This Client has been removed')), fail_silently= True)
        return redirect(reverse('client_task_list', kwargs={'domain_name': domain_name}))
