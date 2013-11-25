from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from vcg.admin_management.models import Caregiver, Client
from vcg.company_management.models import ClientCaregivers, Messages
from vcg.utilities import company_login
from vcg.config import choices

@company_login
def client_caregivers(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    caregivers = ClientCaregivers.objects.filter(client__id = client_id).values_list('caregiver').distinct()
    caregiver_list = Caregiver.objects.filter(id__in = caregivers).order_by('-modified_at')
    
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
    return render_to_response('company/client_caregivers.html', locals(), context_instance=RequestContext(request))

@company_login
def client_caregiver_details(request, domain_name = None, client_id = None, caregiver_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    caregiver_details = Caregiver.objects.get(id = caregiver_id)
    return render_to_response('company/client_caregiver_details.html', locals(), context_instance=RequestContext(request))
