from django.shortcuts import render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.animation_forms import AnimationForm
from vcg.admin_management.models import Animation
from vcg.utilities import Utility, admin_login, permission_view
from vcg.config import choices

@admin_login
@permission_view('ANI1', None)
def animation_add(request, read_only):
    if request.POST:
        form = AnimationForm(request.POST, request.FILES)
        if form.is_valid():
            animation = form.save(commit = False)
            animation.created_by = animation.modified_by = request.user
            animation.save()
            messages.success(request,(_("Animation Saved Successfully")),
                                         fail_silently = True)
            return redirect('/admin_management/animation_list/')
        else:
            return render_to_response('admin/animation_add.html', locals(), context_instance=RequestContext(request))
    else:
        form = AnimationForm()
    return render_to_response('admin/animation_add.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('ANI3', None)
def animation_list(request, read_only):
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        animation_list = Animation.objects.filter(name__icontains = key).order_by('-modified_at')
    else:
        animation_list = Animation.objects.all().order_by('-modified_at')

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
            
    return render_to_response('admin/animation_list.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('ANI2', 'ANI3')
def animation_edit(request, read_only, animate_id = None):
    try:
        try_animation = Animation.objects.get(pk = animate_id)
        selected_animation = get_object_or_404(Animation, pk = animate_id)
        if request.POST:
            form = AnimationForm(request.POST, request.FILES,instance = selected_animation)
            if form.is_valid():
                animate = form.save(commit = False)
                animate.created_by = animate.modified_by = request.user
                animate.save()
                messages.success(request,(_("Animation Edited Successfully")),
                                             fail_silently = True)
                return redirect('/admin_management/animation_list/')
            else:
                return render_to_response('admin/animation_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = AnimationForm(instance = selected_animation)
        return render_to_response('admin/animation_edit.html', locals(), context_instance=RequestContext(request))
    except Animation.DoesNotExist:
        messages.success(request,('This Animation has been removed'), fail_silently= True)
        return redirect('/admin_management/animation_list/')
    
@admin_login
@permission_view('ANI4')
def animation_delete(request, read_only):
    if request.method == 'POST':
        animation_ids    = request.POST.getlist('choices')
        for animation_id in animation_ids:
            animation = Animation.objects.get(id = animation_id)
            animation.delete()
        if len(animation_ids) > 1:
            messages.success(request,(_("Selected Animations Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Animation Deleted Successfully")),fail_silently = True)            
    return redirect('/admin_management/animation_list/')
