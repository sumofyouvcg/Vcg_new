from django.shortcuts import render_to_response, RequestContext, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.utilities import caregiver_login, view_access
from vcg.admin_management.models import Caregiver
from vcg.admin_management.caregivers_forms import CaregiversForm

@caregiver_login
def caregiver_home(request, domain_name = None, comp_id = None):
    return render_to_response('caregiver/caregiver_home.html', locals(), context_instance=RequestContext(request))

@caregiver_login
def my_profile(request, domain_name = None):
    try:
        try_caregiver = Caregiver.objects.get(caregiver_number = request.user.username)
        selected_caregiver = get_object_or_404(Caregiver, caregiver_number = request.user.username)
        old_email = selected_caregiver.email
        if request.POST:
            form = CaregiversForm(request.POST, request.FILES,instance = selected_caregiver)
            if form.is_valid():
                caregiver = form.save(commit = False)
                caregiver.created_by = caregiver.modified_by = request.user
                if not form.files:
                    caregiver.caregiver_image = ''
                caregiver.save()
                User.objects.filter(username = caregiver.caregiver_number).update(first_name = caregiver.name)
                if old_email != caregiver.email:
                    User.objects.filter(email = old_email).update(username = caregiver.caregiver_number, email = caregiver.email)
                messages.success(request,(_("Caregiver edited Successfully")),
                                             fail_silently = True)
                return redirect(reverse('caregiver_tasks', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('caregiver/my_profile.html', locals(), context_instance=RequestContext(request))
        else:
            form = CaregiversForm(instance = selected_caregiver)
        return render_to_response('caregiver/my_profile.html', locals(), context_instance=RequestContext(request))
    except Caregiver.DoesNotExist:
        messages.success(request,(_('This Caregiver has been removed')), fail_silently= True)
        return redirect(reverse('caregiver_tasks', kwargs={'domain_name': domain_name}))