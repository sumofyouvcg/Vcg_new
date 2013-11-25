from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.client_management.client_plan_forms import ClientPlanForm
from vcg.client_management.models import ClientPlan, PlanFeedback
from vcg.client_management.client_plan_forms import PlanFeedbackForm
from vcg.company_management.models import CompanyClientPlan
from vcg.utilities import client_login
from vcg.config import choices

@client_login
def plan_list(request, domain_name = None):  
    plan_list =  CompanyClientPlan.objects.filter(client__client_number = request.user.username, active = True)

    paginate  = Paginator(plan_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        plan_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        plan_list = paginate.page(paginate.num_pages)
    num_pages = range(plan_list.paginator.num_pages)    
    return render_to_response('client/client_plan_list.html', locals(), context_instance = RequestContext(request))

@client_login
def client_plan_view(request, domain_name = None, plan_id = None, another_action = None):
    CompanyClientPlan.objects.filter(id = plan_id).update(assign_status = False)
    try:
        plan = CompanyClientPlan.objects.get(pk = plan_id)
        selected_plan = get_object_or_404(CompanyClientPlan, pk = plan_id)
        exist_feedback = PlanFeedback.objects.filter(plan = plan_id).order_by('created_at')
        if request.POST:
            form = ClientPlanForm(request.POST, request.FILES)
            if form.is_valid():
                plan = form.save(commit = False)
                plan.created_by = plan.modified_by = request.user
                plan.save()
                if another_action == '1':
                    all_actions = ClientPlan.objects.filter(plan = selected_plan)
                    CompanyClientPlan.objects.filter(id = plan_id).update(post_status = True, post_read_status = True)
                    return redirect(reverse('client_plan_view', kwargs={'domain_name': domain_name, 'plan_id':plan_id,'another_action':another_action}))
                else:
                    messages.success(request,(_("Plan Action Saved Successfully")),fail_silently = True)
                    CompanyClientPlan.objects.filter(id = plan_id).update(post_status = True, post_read_status = True)
                    return redirect(reverse('client_plan_list', kwargs={'domain_name': domain_name}))
            else:
                all_actions = ClientPlan.objects.filter(plan = selected_plan)
                form1 = PlanFeedbackForm()
                return render_to_response('client/client_plan_view.html', locals(), context_instance=RequestContext(request))
        else:
            form = ClientPlanForm()
            form1 = PlanFeedbackForm()
            all_actions = ClientPlan.objects.filter(plan = selected_plan)
        return render_to_response('client/client_plan_view.html', locals(), context_instance=RequestContext(request))
    except CompanyClientPlan.DoesNotExist:
        messages.success(request,(_('This Plan has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_plan_list', kwargs={'domain_name': domain_name}))
    
@client_login
def client_plan_feedback(request, domain_name = None, plan_id = None):
    try:
        plan = CompanyClientPlan.objects.get(pk = plan_id)
        selected_plan = get_object_or_404(CompanyClientPlan, pk = plan_id)
        all_actions = ClientPlan.objects.filter(plan = selected_plan)
        exist_feedback = PlanFeedback.objects.filter(plan = plan_id).order_by('created_at')
        if request.method == "POST":
            form = ClientPlanForm()
            form1 = PlanFeedbackForm(request.POST, request.FILES)
            if form1.is_valid():
                feedback = form1.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                
                CompanyClientPlan.objects.filter(id = plan_id).update(assign_status = False, post_status = True, post_read_status = True)
                
                return redirect(reverse('client_plan_list', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('client/client_plan_view.html', locals(), context_instance = RequestContext(request))
            form1 = PlanFeedbackForm()     
        return render_to_response('company/client_plan_view.html', locals(), context_instance = RequestContext(request))
    except CompanyClientPlan.DoesNotExist:
        messages.success(request,(_('This Plan has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_plan_list', kwargs={'domain_name': domain_name}))
    
@client_login
def client_plan_edit(request, domain_name = None, plan_id = None, action_id = None):
    try:
        plan = CompanyClientPlan.objects.get(pk = plan_id)
        selected_plan = get_object_or_404(CompanyClientPlan, pk = plan_id)
        selected_action = get_object_or_404(ClientPlan, pk = action_id)
        if request.method == "POST":
            form = ClientPlanForm(request.POST, request.FILES, instance = selected_action)
            if form.is_valid():
                action = form.save(commit = False)
                action.created_by = action.modified_by = request.user
                action.save()
                messages.success(request,(_("Client Edited Successfully")),fail_silently = True)
                return redirect(reverse('client_plan_view', kwargs={'domain_name': domain_name, 'plan_id':plan_id, 'another_action':0}))
                #return redirect('/client_management/client_plan_view/'+str(plan_id)+'/0/')
            else:
                return render_to_response('client/client_plan_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = ClientPlanForm(instance = selected_action)
        return render_to_response('client/client_plan_edit.html', locals(), context_instance=RequestContext(request))
    except CompanyClientPlan.DoesNotExist:
        messages.success(request,(_('This Plan has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_plan_list', kwargs={'domain_name': domain_name}))
        
@client_login
def client_plan_delete(request, domain_name = None, plan_id = None, action_id = None):
    del_action = ClientPlan.objects.filter(id = action_id)
    if del_action:
        del_action.delete()
    #return redirect('/client_management/client_plan_view/'+str(plan_id)+'/0/')
    return redirect(reverse('client_plan_view', kwargs={'domain_name': domain_name, 'plan_id':plan_id, 'another_action':0}))