from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.utilities import company_login
from vcg.admin_management.models import Company
from vcg.admin_management.company_forms import CompanyForm

@company_login
def company_home(request, domain_name = None, comp_id = None):
    return render_to_response('company/company_home.html', locals(), context_instance=RequestContext(request))

@company_login
def my_profile(request, domain_name = None):
    try:
        Company.objects.get(company_number = request.user.username)
        selected_company = get_object_or_404(Company, company_number = request.user.username)
        old_email = selected_company.email
        if request.POST:
            form = CompanyForm(request.POST, request.FILES,instance = selected_company)
            if form.is_valid():
                company = form.save(commit = False)
                company.created_by = company.modified_by = request.user
    #            if company.from_date > currentdate:
    #                company.active = False
                company.save()
                User.objects.filter(username = company.company_number).update(first_name = company.company_name)
                if old_email != company.email:
                    User.objects.filter(email = old_email).update(username = company.company_number, email = company.email)
                messages.success(request,(_("Company edited Successfully")),
                                             fail_silently = True)
                return redirect(reverse('company_tasks', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('company/my_profile.html', locals(), context_instance=RequestContext(request))
        else:
            form = CompanyForm(instance = selected_company)
        return render_to_response('company/my_profile.html', locals(), context_instance=RequestContext(request))
    except Company.DoesNotExist:
        messages.success(request,(_('This Company has been removed')), fail_silently= True)
        return redirect(reverse('company_tasks', kwargs={'domain_name': domain_name}))
    
    
    return render_to_response('company/my_profile.html', locals(), context_instance=RequestContext(request))
