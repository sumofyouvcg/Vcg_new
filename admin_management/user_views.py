from django.shortcuts import render_to_response, RequestContext, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.user_forms import AdminUserForm, PasswordResetForm
from vcg.config import default_groups, mail, choices
from vcg.utilities import Utility, admin_login, Email, permission_view
from vcg.admin_management.models import AdminUserPermission, AdminUser

@admin_login
def user_list(request):  
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        admin_user_list = AdminUser.objects.filter(Q(first_name__icontains = key)|Q(last_name__icontains = key)|Q(email__icontains = key)|Q(user_id__icontains = key)).order_by('-modified_at')
    else:
        admin_user_list = AdminUser.objects.all().order_by('-modified_at')

    admin_login = []
    if admin_user_list:
        for admin_user in admin_user_list:
            user_id = User.objects.get(username = admin_user.user_id)
            admin_login.append({'email':admin_user.email,'last_login':user_id.last_login}) 
    
    paginate  = Paginator(admin_user_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        admin_user_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        admin_user_list = paginate.page(paginate.num_pages)
    num_pages = range(admin_user_list.paginator.num_pages)
                
    return render_to_response('admin/user_list.html', locals(), context_instance = RequestContext(request))


@admin_login
def user_add(request, comp_id = None):
    select = request.GET.get('query')
    if select:
        names = select.split(",")
    if request.POST:
        form = AdminUserForm(request.POST)
        selected_permissions = request.POST.getlist('choices')
        if form.is_valid() and len(selected_permissions) >= 1:
            admin_user = form.save(commit = False)
            admin_user.created_by = admin_user.modified_by = request.user
            admin_user.save()
# For User Mgnt            
            random_password = Utility().generate_password()
            auth_user = User.objects.create_user(admin_user.user_id, admin_user.email, random_password)
            auth_user.is_active = admin_user.active
            auth_user.is_staff = admin_user.active
            default_groups.ADMIN = Group.objects.get(pk = 5)
            auth_user.groups = list(auth_user.groups.all()) + [default_groups.ADMIN, ]
            auth_user.save()
            if select:
                AdminUserPermission.objects.create(admin_user = admin_user, create_file = select, created_by = request.user, modified_by = request.user)
            else:
                AdminUserPermission.objects.create(admin_user = admin_user, create_file = '', created_by = request.user, modified_by = request.user)
            Email().send_email(mail.USER_CREATION_SUBJECT, mail.ADMIN_USER_CREATION_MSG %(admin_user.first_name, admin_user.user_id, random_password), [admin_user.email], "html")
            messages.success(request, _("User added successfully"), fail_silently=True)
            return redirect('/admin_management/user_list/')
        else:
            if not selected_permissions or len(selected_permissions) < 1:
                module_error = _('Choose atleast 1 permissions')
            return render_to_response('admin/user_add.html', locals(), context_instance=RequestContext(request))
    else:
        form = AdminUserForm()
    return render_to_response('admin/user_add.html', locals(), context_instance=RequestContext(request))

@admin_login
def user_edit(request, user_id = None): 
    select = request.GET.get('query')
    selected_admin = get_object_or_404(AdminUser, pk = user_id)
    edit_admin = AdminUserPermission.objects.get(id = selected_admin.id)
    if select:
        permissions = select.split(",")
    else:
        permissions = edit_admin.create_file.split(",")
    old_email = selected_admin.email
    if request.POST:
        selected_permissions = request.POST.getlist('choices')
        form = AdminUserForm(request.POST, request.FILES,instance = selected_admin)
        if form.is_valid() and len(selected_permissions) >= 1:
            admin_user = form.save(commit = False)
            admin_user.created_by = admin_user.modified_by = request.user
            admin_user.save()
            AdminUserPermission.objects.filter(admin_user = user_id).update(create_file = select, created_by = request.user, modified_by = request.user)
            if old_email != admin_user.email:
                User.objects.filter(email = old_email).update(username = admin_user.user_id, email = admin_user.email)
                Email().send_email(mail.USER_CREATION_SUBJECT, mail.ADMIN_USER_EDIT_MSG %(admin_user.first_name, admin_user.email), [admin_user.email], "html")
            messages.success(request, (_("User edited Successfully")),
                                         fail_silently = True)
            return redirect('/admin_management/user_list')
        else:
            if not selected_permissions or len(selected_permissions) < 1:
                module_error = _('Choose atleast 1 permissions')
            return render_to_response('admin/user_edit.html', locals(), context_instance=RequestContext(request))
    else:
        form = AdminUserForm(instance = selected_admin)
    return render_to_response('admin/user_edit.html', locals(), context_instance=RequestContext(request))


@admin_login
def password_change(request):
    user = get_object_or_404(User,id__iexact=request.user.id)
    form = PasswordChangeForm(user=user)
    if request.method == "POST":
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Password Changed Successfully"), fail_silently=True)
            return HttpResponseRedirect('/admin_management/company_list/')
        else:
            return render_to_response('admin/password_form.html', locals(), context_instance = RequestContext(request))

    return render_to_response('admin/password_form.html', locals(), context_instance = RequestContext(request))

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            admin = AdminUser.objects.filter(user_id = username, active = True)
            super_user = User.objects.filter(username = username)
            if not super_user[0].is_superuser and not admin:
                messages.success(request, _("That UserName doesn't have an associated user account . Are you sure you are registered?"), fail_silently = True)
                return HttpResponseRedirect('/admin_user/logout/')           
            random_password = Utility().generate_password()
            user = User.objects.get(username = username)
            user.set_password(random_password)
            user.save()
            Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_PASSWORD_CHANGE_MSG %(user.username, user.username, random_password), [user.email], "html")
            messages.success(request, _("New Password has been sent to your corresponding Email address"),
                                         fail_silently = True)
            return redirect('/')
        else:
            return render_to_response('password/password_reset_form.html', locals(), context_instance = RequestContext(request))
    form = PasswordResetForm()
    return render_to_response('password/password_reset_form.html', locals(), context_instance = RequestContext(request))

@admin_login
def user_delete(request):
    if request.method == 'POST':
        admin_user_ids    = request.POST.getlist('choices')
        for admin_user_id in admin_user_ids:
            admin_user = AdminUser.objects.get(id = admin_user_id)
            User.objects.filter(username = admin_user.user_id).delete()
            admin_user.delete()
        if len(admin_user_ids) > 1:
            messages.success(request, _("Selected AdminUsers Deleted Successfully"), fail_silently = True)
        else:    
            messages.success(request, _("Selected AdminUser Deleted Successfully"), fail_silently = True)            
    return redirect('/admin_management/user_list/')
