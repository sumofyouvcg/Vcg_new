from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.company_management.models import CompanyForms
from vcg.utilities import client_login
from vcg.config import choices

@client_login
def forms_list(request, domain_name = None):  
    forms_list =  CompanyForms.objects.filter(client__client_number = request.user.username)

    paginate  = Paginator(forms_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        forms_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        forms_list = paginate.page(paginate.num_pages)
    num_pages = range(forms_list.paginator.num_pages)    
    return render_to_response('client/client_forms_list.html', locals(), context_instance = RequestContext(request))

@client_login
def client_forms_view(request, domain_name = None, form_id = None):
    CompanyForms.objects.filter(id = form_id).update(assign_status = False)
    try:
        company_forms = CompanyForms.objects.get(pk = form_id)
        selected_form = get_object_or_404(CompanyForms, pk = form_id)
        
        if selected_form.form == 'Intake Form':
            return redirect(reverse('client_intake_form', kwargs={'domain_name': domain_name, 'form_id' : form_id }))
        if selected_form.form == 'Treatment Agreement Form':
            return redirect(reverse('client_treatment_agreement_form', kwargs={'domain_name': domain_name, 'form_id' : form_id }))
        if selected_form.form == 'Treatment Form':
            return redirect(reverse('client_client_treatment_form', kwargs={'domain_name': domain_name, 'form_id' : form_id }))
        else:
            return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))
    except CompanyForms.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_forms_list', kwargs={'domain_name': domain_name }))