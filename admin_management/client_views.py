from datetime import date

from django.shortcuts import render_to_response, RequestContext, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.client_forms import ClientForm
from vcg.admin_management.models import Client, Company
from vcg.config import default_groups, mail, choices 
from vcg.utilities import Utility, admin_login, Email, permission_view

@admin_login
@permission_view('CLI3', None)
def client_list(request,read_only):
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        client_list = Client.objects.filter(Q(name__icontains = key)|Q(place_name__icontains = key)|Q(zip_code__icontains = key)|Q(address__icontains = key)|Q(phone_number = key)|Q(client_number__icontains = key)|Q(email__icontains = key)).order_by('-modified_at')
    else:
        client_list = Client.objects.filter().order_by('-modified_at')
    
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
    return render_to_response('admin/client_list.html', locals(), context_instance=RequestContext(request))


@admin_login
@permission_view('CLI1', None)
def client_add(request,read_only):
    if request.POST:
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            company_id       =  form.cleaned_data['company'].id 
            comp             = Company.objects.get(id = company_id)  
            no_of_client     = Client.objects.filter(company = comp)
            currentdate = date.today()
            if len(no_of_client) >= comp.number_of_clients:
                messages.success(request,(_("You are authorised to add %s clients Only") % str(comp.number_of_clients)), fail_silently = True)
                return redirect('/admin_management/client_list/')
            if comp.expiry_date < currentdate :                
                messages.success(request,(_("Client could not be added. This Company already expired")), fail_silently = True)
                return redirect('/admin_management/client_list/')
            form.save()
            client = form.save(commit = False)
            client.created_by = client.modified_by = request.user
            client.save()

            # For User Mgnt            
            random_password = Utility().generate_password()
            auth_user = User.objects.create_user(client.client_number, client.email, random_password)
            auth_user.is_active = True
            auth_user.is_staff = True
            auth_user.first_name = client.name
            default_groups.CLIENT = Group.objects.get(pk = 4)
            auth_user.groups = list(auth_user.groups.all()) + [default_groups.CLIENT, ]
            auth_user.save()
            Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_CREATION_MSG %(client.name, client.company.sub_domain, client.client_number, random_password), [client.email], "html")
            messages.success(request,(_("Client Saved Successfully")),fail_silently = True)
            return redirect('/admin_management/client_list')
        else:
            return render_to_response('admin/client_add.html', locals(), context_instance=RequestContext(request))
    else:
        form = ClientForm()
    return render_to_response('admin/client_add.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('CLI2', 'CLI3')
def client_edit(request,read_only, client_id = None): 
    try:
        try_client = Client.objects.get(id = client_id)
        selected_client = get_object_or_404(Client, pk = client_id)
        old_email = selected_client.email
        if request.POST:
            form = ClientForm(request.POST, request.FILES,instance = selected_client)
            if form.is_valid():
                client = form.save(commit = False)
                client.created_by = client.modified_by = request.user
                if not form.files:
                    client.client_image = ''
                client.save()
                User.objects.filter(username = client.client_number).update(first_name = client.name)
                if old_email != client.email:
                    User.objects.filter(email = old_email).update(username = client.client_number, email = client.email)
                    Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_EDIT_MSG %(client.name, client.company.sub_domain, client.client_number), [client.email], "html")
                messages.success(request,(_("Client Edited Successfully")), fail_silently = True)
                return redirect('/admin_management/client_list')
            else:
                return render_to_response('admin/client_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = ClientForm(instance = selected_client)
        return render_to_response('admin/client_edit.html', locals(), context_instance=RequestContext(request))
    except Client.DoesNotExist:
        messages.success(request,(_('This Client has been removed')), fail_silently= True)
        return redirect('/admin_management/client_list/')
    
@admin_login
@permission_view('CLI4')
def client_delete(request, read_only):
    if request.method == 'POST':
        client_ids    = request.POST.getlist('choices')
        for client_id in client_ids:
            client = Client.objects.get(id = client_id)
            User.objects.filter(username = client.client_number).delete()
            client.delete()
        if len(client_ids) > 1:
            messages.success(request, (_("Selected Clients Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request, (_("Selected Client Deleted Successfully")),fail_silently = True)            
    return redirect('/admin_management/client_list/')
