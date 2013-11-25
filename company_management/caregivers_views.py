from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.caregivers_forms import CaregiversForm
from vcg.admin_management.models import Caregiver, Company
from vcg.utilities import Utility, Email, company_login
from vcg.config import default_groups, mail, choices

@company_login
def caregivers_list(request, domain_name = None):
    if request.user.id:
        company_number = request.user.username
        company_id = Company.objects.get(company_number = company_number).id
    if request.POST:
        key = request.POST.get('place')
    else:
        key = request.GET.get('keyword')
    filter_val = request.GET.get('filter')
    
    if filter_val:
        if filter_val=="InActive":
            caregiver_list = Caregiver.objects.filter(active = False, company = company_id).order_by('-modified_at')
        elif filter_val == "All":    
            caregiver_list = Caregiver.objects.filter(company = company_id).order_by('-modified_at')
        else:    
            caregiver_list = Caregiver.objects.filter(company = company_id, role = filter_val).order_by('-modified_at')            
    if key is not None: 
        key = key.lstrip()
    if key :
        caregiver_list = Caregiver.objects.filter(Q(name__icontains = key)|Q(place_name__icontains = key)|Q(zip_code__icontains = key)|Q(address__icontains = key)|Q(phone_number = key)|Q(caregiver_number__icontains = key)|Q(email__icontains = key)|Q(company__company_name__icontains = key), company = company_id).order_by('-modified_at')
    if not filter_val and not key:
        caregiver_list = Caregiver.objects.filter(company = company_id).order_by('-modified_at')
    
    paginate  = Paginator(caregiver_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        caregiver_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        caregiver_list = paginate.page(paginate.num_pages)
    num_pages = range(caregiver_list.paginator.num_pages)  
    
    return render_to_response('company/caregivers_list.html', locals(), context_instance=RequestContext(request))

@company_login
def caregivers_add(request, domain_name = None, company_id = None):
    comp = Company.objects.get(id = company_id)
    form    = CaregiversForm( initial={'company': comp})
    if request.POST:
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
            return redirect(reverse('company_caregivers_list', kwargs={'domain_name': domain_name})) 
        else:
            return render_to_response('company/caregivers_add.html', locals(), context_instance=RequestContext(request))
    else:
        form = CaregiversForm(initial={'company': company_id})
    return render_to_response('company/caregivers_add.html', locals(), context_instance=RequestContext(request))

@company_login
def caregivers_edit(request, domain_name = None, company_id = None, caregiver_id = None): 
    selected_caregiver = get_object_or_404(Caregiver, pk = caregiver_id, company = company_id)
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
            messages.success(request,(_("Caregiver edited Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_caregivers_list', kwargs={'domain_name': domain_name}))
        else:
            return render_to_response('company/caregivers_add.html', locals(), context_instance=RequestContext(request))
    else:
        form = CaregiversForm(instance = selected_caregiver)
    return render_to_response('company/caregivers_add.html', locals(), context_instance=RequestContext(request))


@company_login
def caregivers_delete(request, domain_name = None):
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
    return redirect(reverse('company_caregivers_list', kwargs={'domain_name': domain_name}))

@company_login
def caregiver_view(request, domain_name = None):
    return render_to_response('company/caregiver_view.html', locals(), context_instance=RequestContext(request))

@company_login
def company_caregiver_client(request, domain_name = None):
    return render_to_response('company/company_caregiver_client.html', locals(), context_instance = RequestContext(request))
