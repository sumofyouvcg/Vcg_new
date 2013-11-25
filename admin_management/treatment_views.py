from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponse
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import simplejson
from django.utils.translation import ugettext as _

from vcg.admin_management.treatment_forms import ModuleForm, SessionForm, ModuleAnimationForm
from vcg.admin_management.models import Module, Session, AdminUserPermission, CompanyModules, Client
from vcg.utilities import Utility, admin_login, permission_view
from vcg.config import choices

@admin_login
def treatment(request):
    if request.POST:
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,(_("Module Saved Successfully")),fail_silently = True)
            return render_to_response('admin/treatment.html', locals(), context_instance=RequestContext(request))
        else:
            return render_to_response('admin/add_module.html', locals(), context_instance=RequestContext(request))
    else:
        form = ModuleForm()
    return render_to_response('admin/treatment.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT3', None)
def module_list(request, read_only):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        module_list_page = Module.objects.filter(Q(name__icontains = key)).order_by('-modified_at')
    else:
        module_list_page = Module.objects.all().order_by('-modified_at')

    paginate  = Paginator(module_list_page, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        module_list_page = paginate.page(page)
    except (EmptyPage, InvalidPage):
        module_list_page = paginate.page(paginate.num_pages)
    num_pages = range(module_list_page.paginator.num_pages)
            
    return render_to_response('admin/module_list.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT1', None)
def add_module(request, read_only):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    if request.POST:
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit = False)
            module.created_by = module.modified_by = request.user
            module.save()
            messages.success(request,(_("Module Saved Successfully")),fail_silently = True)
            return redirect('/admin_management/module_list/')
        else:
            return render_to_response('admin/add_module.html', locals(), context_instance=RequestContext(request))
    else:
        form = ModuleForm()
    return render_to_response('admin/add_module.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT2', 'TREAT3')
def edit_module(request, read_only, module_id = None):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    try:
        try_module = Module.objects.get(id = module_id)
        module = get_object_or_404(Module, pk = module_id)
        if request.POST:
            form = ModuleForm(request.POST, request.FILES, instance = module)
            if form.is_valid():
                module = form.save(commit = False)
                module.created_by = module.modified_by = request.user
                module.save()
                messages.success(request,(_("Module Edited Successfully")),fail_silently = True)
                return redirect('/admin_management/module_list/')
            else:
                return render_to_response('admin/add_module.html', locals(), context_instance=RequestContext(request))
        else:
            form = ModuleForm(instance = module)
        return render_to_response('admin/add_module.html', locals(), context_instance=RequestContext(request))
    except Module.DoesNotExist:
        messages.success(request,(_('This Module has been removed')), fail_silently= True)
        return redirect('/admin_management/module_list/')
    
@admin_login
@permission_view('TREAT4')
def module_delete(request, read_only):
    if request.method == 'POST':
        module_ids    = request.POST.getlist('choices')
        for module_id in module_ids:
            module = Module.objects.get(id = module_id)
            module.delete()
        if len(module_ids) > 1:
            messages.success(request,(_("Selected Modules Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Module Deleted Successfully")),fail_silently = True)            
    return redirect('/admin_management/module_list/')

@admin_login
@permission_view('TREAT1', None)
def add_session(request, read_only):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    if request.POST:
        form = SessionForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.save(commit = False)
            session.created_by = session.modified_by = request.user
            session.save()
            messages.success(request,(_("Session Saved Successfully")),fail_silently = True)
            return redirect('/admin_management/add_session/')
        else:
            return render_to_response('admin/add_session.html', locals(), context_instance=RequestContext(request))
    else:
        form = SessionForm()
    return render_to_response('admin/add_session.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT2', 'TREAT3')
def session(request, read_only, session_id = None):
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file
        if not( 'TREAT2' in permission or 'TREAT1' in permission):
            session_view = 'readonly'
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    try:
        try_session = Session.objects.get(id = session_id)
        selected_session = get_object_or_404(Session, pk = session_id)
        if request.method == "POST":
            form = SessionForm(request.POST, request.FILES, instance = selected_session)
            if form.is_valid():
                session = form.save(commit = False)
                session.created_by = session.modified_by = request.user
                session.save()
                messages.success(request,(_("Session Saved Successfully")),fail_silently = True)
                return render_to_response('admin/session.html', locals(), context_instance=RequestContext(request))
            else:
                return render_to_response('admin/session.html', locals(), context_instance=RequestContext(request))
        else:
            form = SessionForm(instance = selected_session)
        return render_to_response('admin/session.html', locals(), context_instance=RequestContext(request))
    except Session.DoesNotExist:
        messages.success(request,(_('This Session has been removed')), fail_silently= True)
        return redirect('/admin_management/module_list/')
    
@admin_login
@permission_view('TREAT4')
def session_delete(request, read_only, session_id = None):
    try:
        try_session = Session.objects.get(id = session_id)
        Session.objects.filter(id = session_id).delete()
        messages.success(request,(_("Session Deleted Successfully")),fail_silently = True)
        return redirect('/admin_management/module_list/')    
    except Session.DoesNotExist:
        messages.success(request,(_('This Session has been removed')), fail_silently= True)
        return redirect('/admin_management/module_list/')
    
@admin_login
@permission_view('TREAT1',None)
def animation_media(request, read_only):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    if request.POST:
        form = ModuleAnimationForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit = False)
            media.created_by = media.modified_by = request.user
            media.active = True
            media.save()
            messages.success(request,(_("Animation Saved Successfully")),fail_silently = True)
            return redirect('/admin_management/animation_media/')
        else:
            return render_to_response('admin/animation_media.html', locals(), context_instance=RequestContext(request))
    else:
        form = ModuleAnimationForm()
    return render_to_response('admin/animation_media.html', locals(), context_instance=RequestContext(request))

@admin_login
def treatment_drag(request, module_id = None, session_id = None):
    try:
        sessions = Session.objects.get(id = session_id)
        module_name = Module.objects.get(id = module_id)
        existing = Session.objects.filter(module = module_id, name = sessions.name)
        if existing:
            newname = 'Sorry'
        else:
            new_name = Session.objects.create(name = sessions.name, module = module_name, plaintext = sessions.plaintext, created_by = request.user, modified_by = request.user)
            newname = new_name.id
        json = simplejson.dumps({'status':'value','message':newname})
        return HttpResponse(json, mimetype = "application/javascript")
    except Session.DoesNotExist:
        messages.success(request,(_('This Session has been removed')), fail_silently= True)
        json = simplejson.dumps({'status':'error','message':_('This session has been removed')})
        return HttpResponse(json, mimetype = "application/javascript")
