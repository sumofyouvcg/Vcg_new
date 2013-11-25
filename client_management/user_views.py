from django.shortcuts import render_to_response, RequestContext, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from vcg.utilities import client_login

@client_login
def password_change(request, domain_name = None):
    user = get_object_or_404(User,id__iexact=request.user.id)
    form = PasswordChangeForm(user=user)
    if request.method == "POST":
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, (_( "Password Changed Successfully")),fail_silently=True)
            return redirect(reverse('client_task_list', kwargs={'domain_name': domain_name}))
        else:
            return render_to_response('client/password_form.html', locals(), context_instance = RequestContext(request))

    return render_to_response('client/password_form.html', locals(), context_instance = RequestContext(request))