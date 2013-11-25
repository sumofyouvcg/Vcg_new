from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.client_management.models import CompanyFormFeedback, ClientIntakeForm
from vcg.client_management.client_intake_forms import ClientIntakeFormForm1, ClientIntakeFormForm2, ClientIntakeFormForm3
from vcg.client_management.client_form_forms import CompanyFormFeedbackForm
from vcg.company_management.models import CompanyForms
from vcg.admin_management.models import Client
from vcg.utilities import client_login

@client_login
def client_intake_form(request, domain_name = None, form_id = None):
    client_name = Client.objects.get(client_number = request.user)
    CompanyForms.objects.filter(id = form_id).update(assign_status = False)
    try:
        company_forms = CompanyForms.objects.get(pk = form_id)
        client_intake = ClientIntakeForm.objects.filter(company_forms = company_forms, client__client_number = request.user.username)
        if client_intake:
            return redirect(reverse('client_intake_form_feedback', kwargs={'domain_name': domain_name, 'intake_id': client_intake[0].id}))
        else:
            if request.POST:
                form1 = ClientIntakeFormForm1(request.POST, request.FILES)
                form2 = ClientIntakeFormForm2(request.POST, request.FILES)
                form3 = ClientIntakeFormForm3(request.POST, request.FILES)
                if form1.is_valid() and form2.is_valid() and form3.is_valid():
                    clientform1 = form1.save(commit = False)
                    clientform1.created_by = clientform1.modified_by = request.user
                    clientform1.save()
                    clientform2 = form2.save(commit = False)
                    clientform2.created_by = clientform2.modified_by = request.user
                    clientform2.save()
                    clientform3 = form3.save(commit = False)
                    clientform3.created_by = clientform3.modified_by = request.user
                    clientform3.save()
                    ClientIntakeForm.objects.create(client = client_name,
                                                    company_forms = company_forms, 
                                                    form1 = clientform1,
                                                    form2 = clientform2,
                                                    form3 = clientform3,
                                                   )
                    messages.success(request,(_("Your Form Sent Successfully")),
                                                 fail_silently = True)
                    
                    CompanyForms.objects.filter(id = form_id).update(assign_status = False, post_status = True, post_read_status = True)
                    return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))
                else:
                    return render_to_response('client/client_intake_forms_view.html', locals(), context_instance=RequestContext(request))   
            else:
                form1 = ClientIntakeFormForm1()
                form2 = ClientIntakeFormForm2()
                form3 = ClientIntakeFormForm3()
        return render_to_response('client/client_intake_forms_view.html', locals(), context_instance=RequestContext(request))
    except CompanyForms.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))
    
@client_login
def client_intake_form_feedback(request, domain_name = None, intake_id = None):
    try:
        intake_form    = ClientIntakeForm.objects.get(id = intake_id)
        form1          = ClientIntakeFormForm1(instance = intake_form.form1)
        form2          = ClientIntakeFormForm2(instance = intake_form.form2)
        form3          = ClientIntakeFormForm3(instance = intake_form.form3)
        exist_feedback = CompanyFormFeedback.objects.filter(client_intake_form = intake_id).order_by('created_at')
        form           = CompanyFormFeedbackForm()
        if request.POST:
            form           = CompanyFormFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.save()
                messages.success(request,(_("Your Feedback Sent Successfully")), fail_silently = True)
                CompanyForms.objects.filter(id = feedback.client_intake_form.company_forms.id).update(assign_status = False, post_status = True, post_read_status = True)
                return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))
            else:
                return render_to_response('client/client_intake_form_feedback.html', locals(), context_instance=RequestContext(request))   
        else:
            return render_to_response('client/client_intake_form_feedback.html', locals(), context_instance=RequestContext(request))   
    except ClientIntakeForm.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))