from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.caregivers_forms import CaregiversForm
from vcg.admin_management.models import Caregiver, Client
from vcg.company_management.models import ClientCaregivers
from vcg.config import default_groups, mail, choices
from vcg.utilities import Utility, admin_login, Email, permission_view


@admin_login
@permission_view('CAR3', None)
def caregivers_list(request, read_only):  
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        caregivers_list = Caregiver.objects.filter(Q(name__icontains = key)|Q(place_name__icontains = key)|Q(zip_code__icontains = key)|Q(address__icontains = key)|Q(phone_number = key)|Q(caregiver_number__icontains = key)|Q(email__icontains = key)|Q(company__company_name__icontains = key)).order_by('-modified_at')
    else:
        caregivers_list = Caregiver.objects.filter().order_by('-modified_at')

    paginate  = Paginator(caregivers_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        caregivers_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        caregivers_list = paginate.page(paginate.num_pages)
    num_pages = range(caregivers_list.paginator.num_pages)
        
    return render_to_response('admin/caregivers_list.html', locals(), context_instance = RequestContext(request))

@admin_login
@permission_view('CAR1', None)
def caregivers_add(request, read_only, comp_id = None):   
    if request.method == "POST":
        form = CaregiversForm(request.POST, request.FILES)
        if form.is_valid():
            caregiver = form.save(commit = False)
            caregiver.created_by = caregiver.modified_by = request.user
            caregiver.save()
# For User Mgnt            
            random_password = Utility().generate_password()
            auth_user = User.objects.create_user(caregiver.caregiver_number, caregiver.email, random_password)
            auth_user.is_active = True
            auth_user.is_staff = True
            auth_user.first_name = caregiver.name
            default_groups.CAREGIVER = Group.objects.get(pk = 3)
            auth_user.groups = list(auth_user.groups.all()) + [default_groups.CAREGIVER, ]
            auth_user.save()
            Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_CREATION_MSG %(caregiver.name, caregiver.company.sub_domain, caregiver.caregiver_number, random_password), [caregiver.email], "html")
            messages.success(request,(_("Caregiver Saved Successfully")),
                                         fail_silently = True)
            return redirect('/admin_management/caregivers_list/')
        else:
            return render_to_response('admin/caregivers_add.html', locals(), context_instance = RequestContext(request))
    else:
        form = CaregiversForm()
    return render_to_response('admin/caregivers_add.html', locals(), context_instance = RequestContext(request))


@admin_login
@permission_view('CAR2', 'CAR3')
def caregivers_edit(request, read_only, caregiver_id = None): 
    try:
        try_caregiver = Caregiver.objects.get(id = caregiver_id)
        selected_caregiver = get_object_or_404(Caregiver, pk = caregiver_id)
        old_email = selected_caregiver.email
        if request.POST:
            form = CaregiversForm(request.POST, request.FILES,instance = selected_caregiver)
            if form.is_valid():
                caregiver = form.save(commit = False)
                caregiver.created_by = caregiver.modified_by = request.user
                if not form.files:
                    caregiver.caregiver_image = ''
                caregiver.save()
                User.objects.filter(username = caregiver.caregiver_number).update(first_name = caregiver.name)
                if old_email != caregiver.email:
                    User.objects.filter(email = old_email).update(username = caregiver.caregiver_number, email = caregiver.email)
                    Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_EDIT_MSG %(caregiver.name, caregiver.company.sub_domain, caregiver.caregiver_number), [caregiver.email], "html")
                messages.success(request,(_("Caregiver edited Successfully")),
                                             fail_silently = True)
                return redirect('/admin_management/caregivers_list')
            else:
                return render_to_response('admin/caregivers_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = CaregiversForm(instance = selected_caregiver)
        return render_to_response('admin/caregivers_edit.html', locals(), context_instance=RequestContext(request))
    except Caregiver.DoesNotExist:
        messages.success(request,(_('This Caregiver has been removed')), fail_silently= True)
        return redirect('/admin_management/caregivers_list/')
    
@admin_login
@permission_view('CAR2', 'CAR3')
def caregiver_client(request, read_only, caregiver_id = None):
    key = request.GET.get('keyword')
    filter_val = request.GET.get('filter')
    try:
        try_caregiver = Caregiver.objects.get(id = caregiver_id)
        clients = ClientCaregivers.objects.filter(caregiver__id = caregiver_id).values_list('client').distinct()
        
        if filter_val:
            if filter_val=="InActive":
                client_list = Client.objects.filter(id__in = clients, active = False).order_by('-modified_at')
            elif filter_val == "All":    
                client_list = Client.objects.filter(id__in = clients, active = True).order_by('-modified_at')
        if key is not None: 
            key = key.lstrip()
        if key :
            client_list = Client.objects.filter(Q(name__icontains = key)|Q(client_number__icontains = key)|Q(email__icontains = key)).order_by('-modified_at')
        if not filter_val and not key:
            client_list = Client.objects.filter(id__in = clients).order_by('-modified_at')
            
        paginate  = Paginator(client_list, choices.list_per_page)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
    
        try:
            client_list = paginate.page(page)
        except (EmptyPage, InvalidPage):
            client_list = paginate.page(paginate.num_pages)
        num_pages = range(client_list.paginator.num_pages)     
        return render_to_response('admin/caregiver_client.html', locals(), context_instance=RequestContext(request))
    except Caregiver.DoesNotExist:
        messages.success(request,(_('This Caregiver has been removed')), fail_silently= True)
        return redirect('/admin_management/caregivers_list/')
    
@admin_login
@permission_view('CAR4')
def caregivers_delete(request, read_only):
    if request.method == 'POST':
        caregiver_ids    = request.POST.getlist('choices')
        for caregiver_id in caregiver_ids:
            caregiver = Caregiver.objects.get(id = caregiver_id)
            User.objects.filter(username = caregiver.caregiver_number).delete()
            caregiver.delete()
        if len(caregiver_ids) > 1:
            messages.success(request,(_("Selected Caregivers Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Caregiver Deleted Successfully")),fail_silently = True)
    return redirect('/admin_management/caregivers_list/')
