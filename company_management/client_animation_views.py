from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Client
from vcg.company_management.client_animation_forms import CompanyClientAnimationForm
from vcg.company_management.models import CompanyClientAnimation, ClientCaregivers, Messages
from vcg.client_management.models import AnimationFeedback
from vcg.client_management.client_animation_forms import AnimationFeedbackForm
from vcg.utilities import company_login
from vcg.config import choices

@company_login
def client_animation_list(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    animation_list = CompanyClientAnimation.objects.filter(client__id = client_id).order_by('-modified_at')
    
    paginate  = Paginator(animation_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        animation_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        animation_list = paginate.page(paginate.num_pages)
    num_pages = range(animation_list.paginator.num_pages)
    return render_to_response('company/client_animation_list.html', locals(), context_instance=RequestContext(request))

@company_login
def client_animation_add(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    form    = CompanyClientAnimationForm(user=request.user, initial={'client': client})
    if request.POST:
        form = CompanyClientAnimationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            animation = form.save(commit = False)
            animation.assign_status = True
            animation.created_by = animation.modified_by = request.user
            animation.save()
            ClientCaregivers.objects.create(client = animation.client , caregiver = animation.caregiver, task_id = "animation_"+str(animation.id), created_by = request.user, modified_by = request.user)
            messages.success(request,(_("Animation Saved Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_client_animation_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
        else:
            return render_to_response('company/client_animation_add.html', locals(), context_instance = RequestContext(request))
    else:
        form    = CompanyClientAnimationForm(user=request.user, initial={'client': client_id})
    return render_to_response('company/client_animation_add.html', locals(), context_instance = RequestContext(request))

@company_login
def client_animation_edit(request, domain_name = None, client_id = None, animation_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        try_animation = CompanyClientAnimation.objects.get(pk = animation_id)
        selected_animation = get_object_or_404(CompanyClientAnimation, pk = animation_id)
        if request.POST:
            form = CompanyClientAnimationForm(request.POST, request.FILES,instance = selected_animation, user=request.user)
            if form.is_valid():
                animation = form.save(commit = False)
                animation.assign_status = True
                animation.created_by = animation.modified_by = request.user
                animation.save()
                ClientCaregivers.objects.filter(client = animation.client, task_id = "animation_"+str(animation.id)).delete()
                ClientCaregivers.objects.create(client = animation.client , caregiver = animation.caregiver, task_id = "animation_"+str(animation.id), created_by = request.user, modified_by = request.user)
                messages.success(request,(_("Animation Edited Successfully")),fail_silently = True)
                return redirect(reverse('company_client_animation_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('company/client_animation_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = CompanyClientAnimationForm(user=request.user, instance = selected_animation)
        return render_to_response('company/client_animation_edit.html', locals(), context_instance=RequestContext(request))
    except CompanyClientAnimation.DoesNotExist:
        messages.success(request,(_('This Animation has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_animation_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_animation_delete(request, domain_name = None, client_id = None):
    if request.method == 'POST':
        company_client_animation_ids    = request.POST.getlist('choices')
        for company_client_animation_id in company_client_animation_ids:
            animation = CompanyClientAnimation.objects.get(id = company_client_animation_id)
            animation.delete()
        if len(company_client_animation_ids) > 1:
            messages.success(request,(_("Selected Animations Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Animation Deleted Successfully")),fail_silently = True)
    return redirect(reverse('company_client_animation_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_animation_view(request, domain_name = None, client_id = None, animation_id = None):
    CompanyClientAnimation.objects.filter(id = animation_id).update(post_read_status = False)
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    try:
        animation = CompanyClientAnimation.objects.get(pk = animation_id)
        selected_animation = get_object_or_404(CompanyClientAnimation, pk = animation_id)
        exist_feedback = AnimationFeedback.objects.filter(animation = animation_id).order_by('created_at')
        if request.method == "POST":
            form = AnimationFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientAnimation.objects.filter(client__id = client_id, pk = animation_id, active = True).update(assign_status = True, post_status = False)
                
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('company_client_animation_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('company/client_animation_view.html', locals(), context_instance = RequestContext(request))
    
        form = AnimationFeedbackForm()
        return render_to_response('company/client_animation_view.html', locals(), context_instance = RequestContext(request))
    except CompanyClientAnimation.DoesNotExist:
        messages.success(request,(_('This Animation has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_animation_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))