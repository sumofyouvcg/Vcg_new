from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Company
from vcg.utilities import company_login
from vcg.company_management.models import ConfigurationContact, ConfigurationLogo, ConfigurationHomepage, ConfigurationLocation
from vcg.company_management.configuration_forms import ConfigurationContactForm, ConfigurationLogoForm, ConfigurationHomepageForm, ConfigurationLocationForm

# client Main tabs
@company_login
def configuration_contact(request, domain_name = None):
    if request.user:
        company_id = Company.objects.get(company_number = request.user.username).id
    config_contact = ConfigurationContact.objects.filter(company__id = company_id)
    if config_contact:
        contact = config_contact[0]
    else:
        contact = []    
    form = ConfigurationContactForm()
    return render_to_response('company/configuration_contact.html', locals(), context_instance=RequestContext(request))

@company_login
def config_contact_update(request, domain_name = None, company_id=None):
    comp = Company.objects.get(id = company_id)
    selected_contact = ConfigurationContact.objects.filter(company__id = company_id)
    form    = ConfigurationContactForm( initial={'company': comp})
    if request.POST:
        if selected_contact:
            form = ConfigurationContactForm(request.POST, request.FILES, instance = selected_contact[0])
        else:
            form = ConfigurationContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit = False)
            contact.created_by = contact.modified_by = request.user
            contact.active = True
            contact.save()
            messages.success(request,(_("Configuration Contact Saved Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_configuration_contact', kwargs={'domain_name': domain_name }))
        else:
            return render_to_response('company/config_contact_update.html', locals(), context_instance=RequestContext(request))
    else:
        if selected_contact:
            form = ConfigurationContactForm(initial={'company': company_id}, instance = selected_contact[0])
        else:
            form = ConfigurationContactForm(initial={'company': company_id})   
               
    return render_to_response('company/config_contact_update.html', locals(), context_instance=RequestContext(request))

@company_login
def configuration_domain(request, domain_name = None):
    if request.user:
        company = Company.objects.get(company_number = request.user.username)
    return render_to_response('company/configuration_domain.html', locals(), context_instance=RequestContext(request))

@company_login
def configuration_layout(request, domain_name = None):
    if request.user:
        company_id = Company.objects.get(company_number = request.user.username).id
    config_logo = ConfigurationLogo.objects.filter(company__id = company_id)
    if config_logo:
        logo = config_logo[0]
    else:
        logo = []    
    form = ConfigurationLogoForm()    
    return render_to_response('company/configuration_layout.html', locals(), context_instance=RequestContext(request))

@company_login
def config_layout_update(request, domain_name = None, company_id=None):
    comp = Company.objects.get(id = company_id)
    selected_logo = ConfigurationLogo.objects.filter(company__id = company_id)
    form    = ConfigurationLogoForm( initial={'company': comp})
    if request.POST:
        if selected_logo:
            form = ConfigurationLogoForm(request.POST, request.FILES, instance = selected_logo[0])
        else:
            form = ConfigurationLogoForm(request.POST, request.FILES)
        if form.is_valid():
            logo = form.save(commit = False)
            logo.created_by = logo.modified_by = request.user
            logo.active = True
            logo.save()
            messages.success(request,(_("Configuration Layout Saved Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_configuration_layout', kwargs={'domain_name': domain_name }))
        else:
            return render_to_response('company/config_layout_update.html', locals(), context_instance=RequestContext(request))
    else:
        if selected_logo:
            form = ConfigurationLogoForm(initial={'company': company_id}, instance = selected_logo[0])
        else:
            form = ConfigurationLogoForm(initial={'company': company_id})   
               
    return render_to_response('company/config_layout_update.html', locals(), context_instance=RequestContext(request))

@company_login
def configuration_home_page(request, domain_name = None):
    if request.user:
        company_id = Company.objects.get(company_number = request.user.username).id
    config_home = ConfigurationHomepage.objects.filter(company__id = company_id)
    if config_home:
        home = config_home[0]
    else:
        home = []    
    form = ConfigurationHomepageForm()    
    return render_to_response('company/configuration_home_page.html', locals(), context_instance=RequestContext(request))

@company_login
def config_homepage_update(request, domain_name = None, company_id=None):
    comp = Company.objects.get(id = company_id)
    selected_logo = ConfigurationHomepage.objects.filter(company__id = company_id)
    form    = ConfigurationHomepageForm( initial={'company': comp})
    if request.POST:
        if selected_logo:
            form = ConfigurationHomepageForm(request.POST, request.FILES, instance = selected_logo[0])
        else:
            form = ConfigurationHomepageForm(request.POST, request.FILES)
        if form.is_valid():
            home = form.save(commit = False)
            home.created_by = home.modified_by = request.user
            home.active = True
            home.save()
            messages.success(request,(_("Configuration Homepage Messages Saved Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_configuration_home_page', kwargs={'domain_name': domain_name }))
        else:
            return render_to_response('company/config_homepage_update.html', locals(), context_instance=RequestContext(request))
    else:
        if selected_logo:
            form = ConfigurationHomepageForm(initial={'company': company_id}, instance = selected_logo[0])
        else:
            form = ConfigurationHomepageForm(initial={'company': company_id})   
               
    return render_to_response('company/config_homepage_update.html', locals(), context_instance=RequestContext(request))

@company_login
def configuration_location(request, domain_name = None):
    if request.user:
        company_id = Company.objects.get(company_number = request.user.username).id
    config_location = ConfigurationLocation.objects.filter(company__id = company_id)
    if config_location:
        location = config_location[0]
    else:
        location = []    
    form = ConfigurationLocationForm()    
    return render_to_response('company/configuration_location.html', locals(), context_instance=RequestContext(request))

@company_login
def config_location_update(request, domain_name = None, company_id=None):
    comp = Company.objects.get(id = company_id)
    selected_location = ConfigurationLocation.objects.filter(company__id = company_id)
    form    = ConfigurationLocationForm( initial={'company': comp})
    if request.POST:
        if selected_location:
            form = ConfigurationLocationForm(request.POST, request.FILES, instance = selected_location[0])
        else:
            form = ConfigurationLocationForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.save(commit = False)
            location.created_by = location.modified_by = request.user
            location.active = True
            location.save()
            messages.success(request,(_("Configuration Loaction Saved Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_configuration_location', kwargs={'domain_name': domain_name }))
            
        else:
            return render_to_response('company/config_location_update.html', locals(), context_instance=RequestContext(request))
    else:
        if selected_location:
            form = ConfigurationLocationForm(initial={'company': company_id}, instance = selected_location[0])
        else:
            form = ConfigurationLocationForm(initial={'company': company_id})   
               
    return render_to_response('company/config_location_update.html', locals(), context_instance=RequestContext(request))