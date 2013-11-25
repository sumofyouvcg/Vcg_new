from django.shortcuts import render_to_response, RequestContext, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages

def password_change(request, domain_name = None):
    user = get_object_or_404(User,id__iexact=request.user.id)
    form = PasswordChangeForm(user=user)
    if request.method == "POST":
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,(_("Password Changed Successfully")),fail_silently=True)
            return redirect(reverse('caregiver_tasks', kwargs={'domain_name': domain_name}))
        else:
            return render_to_response('caregiver/password_form.html', locals(), context_instance = RequestContext(request))

    return render_to_response('caregiver/password_form.html', locals(), context_instance = RequestContext(request))