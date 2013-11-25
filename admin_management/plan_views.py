from django.shortcuts import render_to_response, RequestContext, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.plan_forms import PlanForm
from vcg.admin_management.models import Plan
from vcg.utilities import admin_login, permission_view
from vcg.config import choices

@admin_login
@permission_view('PLA3', None)
def plan_list(request, read_only):
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        plan_list = Plan.objects.filter(title__icontains = key).order_by('-modified_at')
    else:
        plan_list = Plan.objects.filter().order_by('-modified_at')
    
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
    return render_to_response('admin/plan_list.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('PLA1', None)
def plan_add(request, read_only, comp_id = None):
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save(commit = False)
            plan.created_by = plan.modified_by = request.user
            plan.save()
            messages.success(request,(_("Plan Saved Successfully")),fail_silently = True)
            return redirect('/admin_management/plan_list/')
        else:
            return render_to_response('admin/plan_add.html', locals(), context_instance = RequestContext(request))
    else:
        form = PlanForm()
    return render_to_response('admin/plan_add.html', locals(), context_instance = RequestContext(request))

@admin_login
@permission_view('PLA2', 'PLA3')
def plan_edit(request, read_only, plan_id = None): 
    try:
        try_plan = Plan.objects.get(id = plan_id)
        selected_plan = get_object_or_404(Plan, pk = plan_id)
        if request.POST:
            form = PlanForm(request.POST, request.FILES,instance = selected_plan)
            if form.is_valid():
                plan = form.save(commit = False)
                plan.created_by = plan.modified_by = request.user
                plan.save()
                messages.success(request,(_("Plan Edited Successfully")),fail_silently = True)
                return redirect('/admin_management/plan_list')
            else:
                return render_to_response('admin/plan_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = PlanForm(instance = selected_plan)
        return render_to_response('admin/plan_edit.html', locals(), context_instance=RequestContext(request))
    except Plan.DoesNotExist:
        messages.success(request,(_('This Plan has been removed')), fail_silently= True)
        return redirect('/admin_management/plan_list/')
    
@admin_login
@permission_view('PLA4')
def plan_delete(request, read_only):
    if request.method == 'POST':
        plan_ids    = request.POST.getlist('choices')
        for plan_id in plan_ids:
            plan = Plan.objects.get(id = plan_id)
            plan.delete()
        if len(plan_ids) > 1:
            messages.success(request,(_("Selected Plans Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Plan Deleted Successfully")),fail_silently = True)            
    return redirect('/admin_management/plan_list/')
