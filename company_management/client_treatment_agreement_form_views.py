from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from vcg.client_management.models import ClientTreatmentAgreementForm, TreatmentAgreementFeedback
from vcg.client_management.client_treatment_agreement_forms import TreatmentAgreementForm, TreatmentAgreementFeedbackForm
from vcg.client_management.client_form_forms import CompanyFormFeedbackForm
from vcg.company_management.models import CompanyForms, Messages
from vcg.admin_management.models import Client
from vcg.utilities import company_login

@company_login
def client_treatment_agreement_form(request, domain_name = None, client_id = None, form_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    CompanyForms.objects.filter(id = form_id).update(assign_status = False)
    try:
        company_forms = CompanyForms.objects.get(pk = form_id)
        client_treatment_agreement = ClientTreatmentAgreementForm.objects.filter(company_forms = company_forms, client__client_number = client_user.username)
        if client_treatment_agreement:
            return redirect(reverse('company_client_treatment_agreement_form_completed', kwargs={'domain_name': domain_name, 'client_id':client_id, 'form_id':form_id, 'treat_agree_id': client_treatment_agreement[0].id}))
        else:
            form = TreatmentAgreementForm()
        return render_to_response('company/client_treatment_agreement_form.html', locals(), context_instance=RequestContext(request))
    except CompanyForms.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_forms_list', kwargs={'domain_name': domain_name, 'client_id': client_id }))

@company_login
def client_treatment_agreement_form_completed(request, domain_name = None, client_id = None,  form_id = None, treat_agree_id = None):
    try:
        treatment_agreement_form    = ClientTreatmentAgreementForm.objects.get(id = treat_agree_id)
        form                        = TreatmentAgreementForm(instance = treatment_agreement_form.treatment_agreement)
        exist_feedback = TreatmentAgreementFeedback.objects.filter(client_treatment_agreement_form = treat_agree_id).order_by('created_at')
        form1           = TreatmentAgreementFeedbackForm()
        if request.POST:
            form1           = TreatmentAgreementFeedbackForm(request.POST)
            if form1.is_valid():
                feedback = form1.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.save()
                messages.success(request,(_("Your Feedback Sent Successfully")), fail_silently = True)
                CompanyForms.objects.filter(id = feedback.client_treatment_agreement_form.company_forms.id).update(assign_status = False, post_status = True, post_read_status = True)
                return redirect(reverse('company_client_forms_list', kwargs={'domain_name': domain_name, 'client_id': client_id }))
            else:
                return render_to_response('company/client_treatment_agreement_form_completed.html', locals(), context_instance=RequestContext(request))   
        else:
            return render_to_response('company/client_treatment_agreement_form_completed.html', locals(), context_instance=RequestContext(request))   
    except ClientTreatmentAgreementForm.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_forms_list', kwargs={'domain_name': domain_name, 'client_id': client_id }))
