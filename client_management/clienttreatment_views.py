from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.company_management.models import ClientTreatmentSessions, ClientSessionsFeedback, CompanyClientTreatment, CompanyModules
from vcg.company_management.client_treatment_forms import ClientSessionsFeedbackForm
from vcg.admin_management.models import Client, Company
from vcg.utilities import client_login
from vcg.config import choices

@client_login
def treatment_list(request, domain_name = None):
    client_name = Client.objects.get(client_number = request.user.username)
    client_treatments = CompanyClientTreatment.objects.filter(client__id = client_name.id, active = True).order_by('-modified_at')
    paginate  = Paginator(client_treatments, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        client_treatments = paginate.page(page)
    except (EmptyPage, InvalidPage):
        client_treatments = paginate.page(paginate.num_pages)
    num_pages = range(client_treatments.paginator.num_pages)
    return render_to_response('client/treatment_list.html', locals(), context_instance=RequestContext(request))

@client_login
def treatment_view(request, domain_name = None, module_id = None):
    client_name = Client.objects.get(client_number = request.user)
    client_id = client_name.id
    
    active_session = request.GET.get('query')
    if active_session:
        session_act = ClientTreatmentSessions.objects.filter(client_treatment = module_id, client = client_id, sessions = active_session)
        session_act.update(activate_session = True)
    completed_session = request.GET.get('complete')
    if completed_session:
        session_act = ClientTreatmentSessions.objects.filter(client_treatment = module_id, client = client_id, sessions = completed_session)
        session_act.update(completed = True)
    make_unaccompany = request.GET.get('make')
    if make_unaccompany:
        session_act = ClientTreatmentSessions.objects.filter(client_treatment = module_id, client = client_id, sessions = make_unaccompany)
        if session_act[0].make_unaccompanied:
            accompany = False
        else:
            accompany = True
        session_act.update(make_unaccompanied = accompany)
    try:
        company_client = CompanyClientTreatment.objects.get(id = module_id, client = client_id)
        total_sessions = ClientTreatmentSessions.objects.filter(client_treatment = module_id, client = client_id).order_by('created_at')
        paginate  = Paginator(total_sessions, choices.list_per_page)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
    
        try:
            total_sessions = paginate.page(page)
        except (EmptyPage, InvalidPage):
            total_sessions = paginate.page(paginate.num_pages)
        num_pages = range(total_sessions.paginator.num_pages)
    except CompanyClientTreatment.DoesNotExist:
        messages.success(request,(_('This treatment has been removed by company')), fail_silently= True)
        return redirect(reverse('client_treatment_list', kwargs={'domain_name': domain_name}))
    return render_to_response('client/client_treatment_view.html', locals(), context_instance=RequestContext(request))

@client_login
def treatment_session(request, domain_name = None, session_id = None):
    ClientTreatmentSessions.objects.filter(id = session_id).update(assign_status = False)
    
    client_name = Client.objects.get(client_number = request.user)
    client_id = client_name.id
    company = Company.objects.get(company_number = client_name.company.company_number)
    try:
        session = ClientTreatmentSessions.objects.get(id = session_id, client = client_id)
        exist_feedback = ClientSessionsFeedback.objects.filter(treatment_session = session.id, client = client_id).order_by('created_at')
        if request.method == "POST":
            form = ClientSessionsFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                ClientTreatmentSessions.objects.filter(id = session_id).update(assign_status = False, post_status = True, post_read_status = True)
                #CompanyClientTreatment.objects.filter(client__id = client_name.id, id = session.client_treatment.id, active = True).update(module_active_status = False, module_post_status = True)
                
                messages.success(request,(_("Reply Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('client_treatment_view', kwargs={'domain_name': domain_name, 'module_id':str(session.client_treatment.id)}))
            else:
                return render_to_response('client/client_treatment_session.html', locals(), context_instance = RequestContext(request))
        else:
            form = ClientSessionsFeedbackForm()
    except ClientTreatmentSessions.DoesNotExist:
        messages.success(request,(_('This session has been removed by company')), fail_silently= True)
        return redirect(reverse('client_treatment_list', kwargs={'domain_name': domain_name}))
    return render_to_response('client/client_treatment_session.html', locals(), context_instance = RequestContext(request))