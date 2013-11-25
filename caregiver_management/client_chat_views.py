from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.db.models import Q

from vcg.client_management.models import ChatMessage
from vcg.admin_management.models import Client
from vcg.utilities import caregiver_login
from vcg.config import choices

@caregiver_login
def chat_details(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    chat_messages = ChatMessage.objects.filter(Q(sender = client_user.id, receiver = request.user)|Q(receiver = client_user.id, sender = request.user)).order_by('received_at')
    caregiver_chat = chat_messages.extra({'received_at' : "date(received_at)"}).values('received_at').distinct()
    paginate  = Paginator(caregiver_chat, choices.list_per_page)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        caregiver_chat = paginate.page(page)
    except (EmptyPage, InvalidPage):
        caregiver_chat = paginate.page(paginate.num_pages)
    num_pages = range(caregiver_chat.paginator.num_pages)
    return render_to_response('caregiver/chat_details.html', locals(), context_instance = RequestContext(request))

@caregiver_login
def chat_history(request, domain_name = None, client_id = None, date = None):
    chat_date = str(date)
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    chat_messages = ChatMessage.objects.filter(Q(sender = client_user.id, receiver = request.user)|Q(receiver = client_user.id, sender = request.user), received_at__startswith = str(date)).order_by('received_at')
    
    paginate  = Paginator(chat_messages, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        chat_messages = paginate.page(page)
    except (EmptyPage, InvalidPage):
        chat_messages = paginate.page(paginate.num_pages)
    num_pages = range(chat_messages.paginator.num_pages)
    return render_to_response('caregiver/chat_history.html', locals(), context_instance = RequestContext(request))