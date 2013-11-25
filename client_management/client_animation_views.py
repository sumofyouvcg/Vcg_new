from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.client_management.models import AnimationFeedback
from vcg.client_management.client_animation_forms import AnimationFeedbackForm
from vcg.company_management.models import CompanyClientAnimation
from vcg.utilities import client_login
from vcg.config import choices

@client_login
def animation_list(request, domain_name = None):  
    animation_list =  CompanyClientAnimation.objects.filter(client__client_number = request.user.username, active = True)

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
    return render_to_response('client/client_animation_list.html', locals(), context_instance = RequestContext(request))

@client_login
def client_animation_view(request, domain_name = None, animation_id = None):
    CompanyClientAnimation.objects.filter(id = animation_id).update(assign_status = False)
    try:
        animation = CompanyClientAnimation.objects.get(pk = animation_id)
        selected_animation = get_object_or_404(CompanyClientAnimation, pk = animation_id)
        exist_feedback = AnimationFeedback.objects.filter(animation = animation_id).order_by('created_at')
        form = AnimationFeedbackForm()
        if request.method == "POST":
            form = AnimationFeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                
                CompanyClientAnimation.objects.filter(id = animation_id).update(assign_status = False, post_status = True, post_read_status = True)
                return redirect(reverse('client_animation_list', kwargs={'domain_name': domain_name }))
            else:
                return render_to_response('client/client_animation_view.html', locals(), context_instance=RequestContext(request))
        return render_to_response('client/client_animation_view.html', locals(), context_instance=RequestContext(request))
    except CompanyClientAnimation.DoesNotExist:
        messages.success(request,(_('This Animation has been removed by Admin')), fail_silently= True)
        return redirect(reverse('client_animation_list', kwargs={'domain_name': domain_name }))
    