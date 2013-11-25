from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Client, Caregiver
from vcg.company_management.company_form_forms import CompanyFormsForm
from vcg.company_management.models import CompanyForms, ClientCaregivers, Messages

from vcg.utilities import caregiver_login, view_access, company_access
from vcg.config import choices

@caregiver_login
@view_access
def client_forms_list(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False   

    form_list = CompanyForms.objects.filter(client__id = client_id).order_by('-modified_at')
    
    paginate  = Paginator(form_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        form_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        form_list = paginate.page(paginate.num_pages)
    num_pages = range(form_list.paginator.num_pages)
    return render_to_response('caregiver/client_forms_list.html', locals(), context_instance=RequestContext(request))

@caregiver_login
@company_access
def client_forms_add(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False   

    form    = CompanyFormsForm(user=request.user, initial={'client': client})
    if request.POST:
        form = CompanyFormsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            forms = form.save(commit = False)
            forms.assign_status = True
            forms.created_by = forms.modified_by = request.user
            forms.save()
            ClientCaregivers.objects.create(client = forms.client , caregiver = forms.caregiver, task_id = "forms_"+str(forms.id), created_by = request.user, modified_by = request.user)
            messages.success(request,(_("Form Saved Successfully")),
                                         fail_silently = True)
            return redirect(reverse('caregiver_client_forms_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
        else:
            return render_to_response('caregiver/client_forms_add.html', locals(), context_instance = RequestContext(request))
    else:
        form    = CompanyFormsForm(user=request.user, initial={'client': client_id})
    return render_to_response('caregiver/client_forms_add.html', locals(), context_instance = RequestContext(request))

@caregiver_login
@company_access
def client_forms_edit(request, domain_name = None, client_id = None, form_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False   
    
    try:
        try_company_form = CompanyForms.objects.get(pk = form_id)
        selected_company_form = get_object_or_404(CompanyForms, pk = form_id)
        if request.POST:
            form = CompanyFormsForm(request.POST, request.FILES,instance = selected_company_form, user=request.user)
            if form.is_valid():
                company_form = form.save(commit = False)
                company_form.assign_status = True
                company_form.created_by = company_form.modified_by = request.user
                company_form.save()
                ClientCaregivers.objects.filter(client = company_form.client, task_id = "forms_"+str(company_form.id)).delete()
                ClientCaregivers.objects.create(client = company_form.client , caregiver = company_form.caregiver, task_id = "form_"+str(company_form.id), created_by = request.user, modified_by = request.user)
                messages.success(request,(_("Form Edited Successfully")),fail_silently = True)
                return redirect(reverse('caregiver_client_forms_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('caregiver/client_forms_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = CompanyFormsForm(user=request.user, instance = selected_company_form)
        return render_to_response('caregiver/client_forms_edit.html', locals(), context_instance=RequestContext(request))
    except CompanyForms.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_forms_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@caregiver_login
@company_access
def client_forms_delete(request, domain_name = None, client_id = None):
    if request.method == 'POST':
        company_client_form_ids    = request.POST.getlist('choices')
        for company_client_form_id in company_client_form_ids:
            company_form = CompanyForms.objects.get(id = company_client_form_id)
            company_form.delete()
        if len(company_client_form_ids) > 1:
            messages.success(request,(_("Selected Forms Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Form Deleted Successfully")),fail_silently = True)
    return redirect(reverse('caregiver_client_forms_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@caregiver_login
@company_access
def client_forms_view(request, domain_name = None, client_id = None, form_id = None):
    CompanyForms.objects.filter(id = form_id).update(post_read_status = False)
    
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        company_forms = CompanyForms.objects.get(pk = form_id)
        selected_form = get_object_or_404(CompanyForms, pk = form_id)
        print selected_form.form
        if selected_form.form == 'Intake Form':
            return redirect(reverse('caregiver_client_intake_form', kwargs={'domain_name': domain_name, 'client_id':client_id, 'form_id' : form_id }))
        elif selected_form.form == 'Treatment Form':
            return redirect(reverse('caregiver_client_treatment_form', kwargs={'domain_name': domain_name, 'client_id':client_id, 'form_id' : form_id }))
        elif selected_form.form == 'Treatment Agreement Form':
            return redirect(reverse('caregiver_client_treatment_agreement_form', kwargs={'domain_name': domain_name, 'client_id':client_id, 'form_id' : form_id }))
        else:
            return redirect(reverse('caregiver_client_forms_list', kwargs={'domain_name': domain_name, 'client_id':client_id  }))
    except CompanyForms.DoesNotExist:
        messages.success(request,(_('This Form has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_forms_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
    