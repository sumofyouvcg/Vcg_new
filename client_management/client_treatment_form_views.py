from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from vcg.client_management.models import TreatmentForm, CompanyTreatmentForm, CompanyTreatmentFormFeedback, MethodsTechniques, DomainYes, IndicatorTreatment
from vcg.client_management.client_treatment_form_forms import TreatmentFormForm, CompanyTreatmentFormFeedbackForm
from vcg.client_management.client_form_forms import CompanyFormFeedbackForm
from vcg.company_management.models import CompanyForms, Messages
from vcg.admin_management.models import Client,Caregiver
from vcg.utilities import client_login

@client_login
def client_treatment_form(request, domain_name = None, form_id = None):
    client_name = Client.objects.get(client_number = request.user)
    client_user = User.objects.get(username = client_name.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    CompanyForms.objects.filter(id = form_id).update(assign_status = False)
    try:
        company_forms = CompanyForms.objects.get(pk = form_id)
        client_treatment_agreement = CompanyTreatmentForm.objects.filter(company_forms = company_forms, client__client_number = client_user.username)
        
        if client_treatment_agreement:
            return redirect(reverse('client_client_treatment_form_completed', kwargs={'domain_name': domain_name, 'treat_id': client_treatment_agreement[0].id}))
        else:
            if request.POST:
                form = TreatmentFormForm(request.POST, request.FILES)
                if form.is_valid():
                    clientform = form.save(commit = False)
                    clientform.created_by = clientform.modified_by = request.user
                    clientform.save()
                    
                    for method in request.POST.getlist(_('methods_techniques')):
                        techniques = MethodsTechniques.objects.create(methods_tech = method, created_by = request.user, modified_by = request.user)
                        clientform.methods_techniques.add(method)
                        
                    for domain in request.POST.getlist(_('domains_yes')):
                        yes = DomainYes.objects.create(domain = domain, created_by = request.user, modified_by = request.user)
                        clientform.domains_yes.add(domain)
                        
                    for indicator in request.POST.getlist(_('indicator_treatment')):
                        indicate = IndicatorTreatment.objects.create(indicator_treat = indicator, created_by = request.user, modified_by = request.user)
                        clientform.indicator_treatment.add(indicator)
                    
                    CompanyTreatmentForm.objects.create(client = client_name,
                                                    company_forms = company_forms, 
                                                    treatment_form = clientform,
                                                    created_by = request.user, 
                                                    modified_by = request.user
                                                   )
                    messages.success(request,(_("Your Form Sent Successfully")),
                                                 fail_silently = True)
                    
                    CompanyForms.objects.filter(id = form_id).update(assign_status = False, post_status = True, post_read_status = True)
                    return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name}))
                else:
                    return render_to_response('client/client_treatment_form.html', locals(), context_instance=RequestContext(request))   
            else:
                form = TreatmentFormForm()
        return render_to_response('client/client_treatment_form.html', locals(), context_instance=RequestContext(request))
    except CompanyForms.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name}))

@client_login
def client_treatment_form_completed(request, domain_name = None,  treat_id = None):
    try:
        treatment_form    = CompanyTreatmentForm.objects.get(id = treat_id)
        form1             = TreatmentFormForm(instance = treatment_form.treatment_form)
        
        client_name = Client.objects.get(client_number = request.user)
        client_user = User.objects.get(username = client_name.client_number)
        new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

        exist_feedback = CompanyTreatmentFormFeedback.objects.filter(company_treatment_form = treat_id).order_by('created_at')
        form           = CompanyTreatmentFormFeedbackForm()
        if request.POST:
            form           = CompanyTreatmentFormFeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.save()
                messages.success(request,(_("Your Feedback Sent Successfully")), fail_silently = True)
                CompanyForms.objects.filter(id = feedback.company_treatment_form.company_forms.id).update(assign_status = False, post_status = True, post_read_status = True)
                return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('client/client_treatment_form_completed.html', locals(), context_instance=RequestContext(request))   
        else:
            return render_to_response('client/client_treatment_form_completed.html', locals(), context_instance=RequestContext(request))   
    except CompanyTreatmentForm.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))