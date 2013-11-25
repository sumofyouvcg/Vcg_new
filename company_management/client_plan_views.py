from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Client
from vcg.company_management.client_plan_forms import CompanyClientPlanForm
from vcg.company_management.models import CompanyClientPlan, ClientCaregivers, Messages
from vcg.client_management.models import ClientPlan, PlanFeedback
from vcg.client_management.client_plan_forms import PlanFeedbackForm
from vcg.utilities import company_login
from vcg.config import choices

@company_login
def client_plan_list(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    p_plans = CompanyClientPlan.objects.filter(client__id = client_id).order_by('-modified_at')
    
    paginate  = Paginator(p_plans, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        p_plans = paginate.page(page)
    except (EmptyPage, InvalidPage):
        p_plans = paginate.page(paginate.num_pages)
    num_pages = range(p_plans.paginator.num_pages)
    return render_to_response('company/client_plan_list.html', locals(), context_instance=RequestContext(request))

@company_login
def client_plan_add(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    form    = CompanyClientPlanForm(user=request.user, initial={'client': client})
    if request.POST:
        form = CompanyClientPlanForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            plan = form.save(commit = False)
            plan.assign_status = True
            plan.created_by = plan.modified_by = request.user
            plan.save()
            ClientCaregivers.objects.create(client = plan.client , caregiver = plan.caregiver, task_id = "plan_"+str(plan.id), created_by = request.user, modified_by = request.user)
            messages.success(request,(_("Practise Plan Saved Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_client_plan_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
        else:
            return render_to_response('company/client_plan_add.html', locals(), context_instance = RequestContext(request))
    else:
        form    = CompanyClientPlanForm(user=request.user, initial={'client': client_id})
    return render_to_response('company/client_plan_add.html', locals(), context_instance = RequestContext(request))

@company_login
def client_plan_edit(request, domain_name = None, client_id = None, plan_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        try_plan = CompanyClientPlan.objects.get(pk = plan_id)
        selected_plan = get_object_or_404(CompanyClientPlan, pk = plan_id)
        if request.POST:
            form = CompanyClientPlanForm(request.POST, request.FILES,instance = selected_plan, user=request.user)
            if form.is_valid():
                plan = form.save(commit = False)
                plan.assign_status = True
                plan.created_by = plan.modified_by = request.user
                plan.save()
                ClientCaregivers.objects.filter(client = plan.client, task_id = "plan_"+str(plan.id)).delete()
                ClientCaregivers.objects.create(client = plan.client , caregiver = plan.caregiver, task_id = "plan_"+str(plan.id), created_by = request.user, modified_by = request.user)
                messages.success(request,(_("Client Edited Successfully")),fail_silently = True)
                return redirect(reverse('company_client_plan_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('company/client_plan_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = CompanyClientPlanForm(user=request.user, instance = selected_plan)
        return render_to_response('company/client_plan_edit.html', locals(), context_instance=RequestContext(request))
    except CompanyClientPlan.DoesNotExist:
        messages.success(request,(_('This Plan has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_plan_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_plan_delete(request, domain_name = None, client_id = None):
    if request.method == 'POST':
        company_client_plan_ids    = request.POST.getlist('choices')
        for company_client_plan_id in company_client_plan_ids:
            plan = CompanyClientPlan.objects.get(id = company_client_plan_id)
            plan.delete()
        if len(company_client_plan_ids) > 1:
            messages.success(request,(_("Selected Plans Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Plan Deleted Successfully")),fail_silently = True)
    return redirect(reverse('company_client_plan_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_plan_view(request, domain_name = None, client_id = None, plan_id = None):
    CompanyClientPlan.objects.filter(id = plan_id).update(post_read_status = False)
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    try:
        plan = CompanyClientPlan.objects.get(pk = plan_id)
        selected_plan = get_object_or_404(CompanyClientPlan, pk = plan_id)
        all_actions = ClientPlan.objects.filter(plan = selected_plan)
        exist_feedback = PlanFeedback.objects.filter(plan = plan_id).order_by('created_at')
        if request.method == "POST":
            form = PlanFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientPlan.objects.filter(client__id = client_id, pk = plan_id, active = True).update(assign_status = True, post_status = False)
                
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('company_client_plan_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))            
            else:
                return render_to_response('company/client_plan_view.html', locals(), context_instance = RequestContext(request))
    
        form = PlanFeedbackForm()
        return render_to_response('company/client_plan_view.html', locals(), context_instance = RequestContext(request))
    except CompanyClientPlan.DoesNotExist:
        messages.success(request,(_('This Plan has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_plan_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))    