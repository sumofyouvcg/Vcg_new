from django.shortcuts import render_to_response, RequestContext, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.utilities import company_login
from vcg.admin_management.user_forms import PasswordResetForm
from vcg.admin_management.models import Company, Caregiver,  Client
from vcg.utilities import Utility, Email
from vcg.config import mail

@company_login
def password_change(request, domain_name = None):
    user = get_object_or_404(User,id__iexact=request.user.id)
    form = PasswordChangeForm(user=user)
    if request.method == "POST":
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,(_("Password Changed Successfully")),fail_silently=True)
            return redirect(reverse('company_tasks', kwargs={'domain_name': domain_name}))
        else:
            return render_to_response('company/password_form.html', locals(), context_instance = RequestContext(request))

    return render_to_response('company/password_form.html', locals(), context_instance = RequestContext(request))

def password_reset(request, domain_name):
    if request.method == "POST":
        form = PasswordResetForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            company = Company.objects.filter(company_number = username, sub_domain = domain_name,  active = True)
            caregiver = Caregiver.objects.filter(caregiver_number = username, company__sub_domain = domain_name, active = True, company__active = True)
            client = Client.objects.filter(client_number = username,company__sub_domain = domain_name, active = True, company__active = True)
            if not company and not caregiver and not client:
                messages.success(request,(_("That UserName doesn't have an associated user account . Are you sure you are registered Under this Domain?")), fail_silently = True)
                return HttpResponseRedirect('/'+domain_name+'/logout/')           
            random_password = Utility().generate_password()
            user = User.objects.get(username = username)
            user.set_password(random_password)
            user.save()
            Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_PASSWORD_CHANGE_MSG %(user.username, user.username, random_password), [user.email], "html")
            messages.success(request,(_("New Password has been sent to your corrosponding Email address")),
                                         fail_silently = True)
            return HttpResponseRedirect('/'+domain_name+'/logout/')  
        else:
            return render_to_response('password/password_reset_form.html', locals(), context_instance = RequestContext(request))
    form = PasswordResetForm()
    return render_to_response('password/password_reset_form.html', locals(), context_instance = RequestContext(request))
