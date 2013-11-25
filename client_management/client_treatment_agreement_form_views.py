from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.client_management.models import ClientTreatmentAgreementForm, TreatmentAgreementFeedback
from vcg.client_management.client_treatment_agreement_forms import TreatmentAgreementForm, TreatmentAgreementFeedbackForm
from vcg.client_management.client_form_forms import CompanyFormFeedbackForm
from vcg.company_management.models import CompanyForms
from vcg.admin_management.models import Client
from vcg.utilities import client_login

@client_login
def client_treatment_agreement_form(request, domain_name = None, form_id = None):
    client_name = Client.objects.get(client_number = request.user)
    CompanyForms.objects.filter(id = form_id).update(assign_status = False)
    try:
        company_forms = CompanyForms.objects.get(pk = form_id)
        client_treat_agree = ClientTreatmentAgreementForm.objects.filter(company_forms = company_forms, client__client_number = request.user.username)
        if client_treat_agree:
            print"first", client_treat_agree
            return redirect(reverse('client_treatment_agreement_form_feedback', kwargs={'domain_name': domain_name, 'treat_agree_id': client_treat_agree[0].id}))
        else:
            if request.POST:
                form = TreatmentAgreementForm(request.POST, request.FILES)
                if form.is_valid():
                    clientform = form.save(commit = False)
                    clientform.created_by = clientform.modified_by = request.user
                    clientform.save()
                    ClientTreatmentAgreementForm.objects.create(client = client_name,
                                                    company_forms = company_forms, 
                                                    treatment_agreement = clientform,
                                                   )
                    messages.success(request,(_("Your Form Sent Successfully")),fail_silently = True)
                    CompanyForms.objects.filter(id = form_id).update(assign_status = False, post_status = True, post_read_status = True)
                    return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))
                else:
                    return render_to_response('client/client_treatment_agreement_forms_view.html', locals(), context_instance=RequestContext(request))   
            else:
                form = TreatmentAgreementForm()
        return render_to_response('client/client_treatment_agreement_forms_view.html', locals(), context_instance=RequestContext(request))
    except CompanyForms.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))
    
@client_login
def client_treatment_agreement_form_feedback(request, domain_name = None, treat_agree_id = None):
    try:
        treatment_agreement_form    = ClientTreatmentAgreementForm.objects.get(id = treat_agree_id)
        print"second", treatment_agreement_form
        form          = TreatmentAgreementForm(instance = treatment_agreement_form.treatment_agreement)
        exist_feedback = TreatmentAgreementFeedback.objects.filter(client_treatment_agreement_form = treat_agree_id).order_by('created_at')
        form1           = TreatmentAgreementFeedbackForm()
        if request.POST:
            form           = TreatmentAgreementFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.save()
                messages.success(request,(_("Your Feedback Sent Successfully")), fail_silently = True)
                CompanyForms.objects.filter(id = feedback.client_treatment_agreement_form.company_forms.id).update(assign_status = False, post_status = True, post_read_status = True)
                return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))
            else:
                return render_to_response('client/client_treatment_agreement_form_feedback.html', locals(), context_instance=RequestContext(request))   
        else:
            return render_to_response('client/client_treatment_agreement_form_feedback.html', locals(), context_instance=RequestContext(request))   
    except ClientTreatmentAgreementForm.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))