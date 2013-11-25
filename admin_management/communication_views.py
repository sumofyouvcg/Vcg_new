from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from vcg.utilities import Utility, admin_login
from vcg.admin_management.models import Company
from vcg.client_management.models import ChatMessage
from vcg.config import choices

@admin_login
def communication(request):
    companys = Company.objects.all()
    comp_list = []
    for company in companys:
        comp_list.append(company.company_number)
    company_users = User.objects.filter(username__in = comp_list)
    return render_to_response('admin/communication.html', locals(), context_instance = RequestContext(request))

@admin_login
def chat_details(request, comp_user_id = None):
    companys = Company.objects.all()
    comp_list = []
    for company in companys:
        comp_list.append(company.company_number)
    company_users = User.objects.filter(username__in = comp_list)

    comp_name = User.objects.get(id = comp_user_id)
    chat_messages = ChatMessage.objects.filter(Q(sender = comp_user_id)|Q(receiver = comp_user_id)).order_by('received_at')
    client_chat_history = chat_messages.extra({'received_at' : "date(received_at)"}).values('received_at').distinct()
    paginate  = Paginator(client_chat_history, choices.list_per_page)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        client_chat_history = paginate.page(page)
    except (EmptyPage, InvalidPage):
        client_chat_history = paginate.page(paginate.num_pages)
    num_pages = range(client_chat_history.paginator.num_pages)
    return render_to_response('admin/chat_details.html', locals(), context_instance = RequestContext(request))



@admin_login
def chat_persons(request, comp_user_id = None, date = None):
    companys = Company.objects.all()
    comp_list = []
    for company in companys:
        comp_list.append(company.company_number)
    company_users = User.objects.filter(username__in = comp_list)

    comp_name = User.objects.get(id = comp_user_id)
    chat_date = str(date)
    chat_messages = ChatMessage.objects.filter(Q(sender = comp_user_id)|Q(receiver = comp_user_id), received_at__startswith = str(date)).order_by('received_at')
    chat_person = []
    for chat in chat_messages:
        if comp_name == chat.sender and chat.receiver.id not in chat_person:
            chat_person.append(chat.receiver.id)
        elif comp_name == chat.receiver and chat.sender.id not in chat_person:
            chat_person.append(chat.sender.id)
    user_list = User.objects.filter(id__in = chat_person)
    
    paginate  = Paginator(user_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        user_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        user_list = paginate.page(paginate.num_pages)
    num_pages = range(user_list.paginator.num_pages)
    return render_to_response('admin/chat_persons.html', locals(), context_instance = RequestContext(request))

@admin_login
def chat_history(request, comp_user_id, date = None, user_id = None):
    companys = Company.objects.all()
    comp_list = []
    for company in companys:
        comp_list.append(company.company_number)
    company_users = User.objects.filter(username__in = comp_list)
    comp_name = User.objects.get(id = comp_user_id)
    
    chat_user = User.objects.get(id = user_id)
    chat_messages = ChatMessage.objects.filter(Q(sender = comp_user_id, receiver = user_id )|Q(receiver = comp_user_id, sender = user_id), received_at__startswith = str(date)).order_by('received_at')
    
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
    return render_to_response('admin/chat_history.html', locals(), context_instance = RequestContext(request))

@admin_login
def chat_date(request,chat=None):
    return render_to_response('admin/chat_date.html', locals(), context_instance = RequestContext(request))

@admin_login
def communication_settings(request):
    return render_to_response('admin/communication_settings.html', locals(), context_instance = RequestContext(request))

@admin_login
def chat(request,chat=None):
    return render_to_response('admin/chat.html', locals(), context_instance = RequestContext(request))

@admin_login
def offline_messages(request,msg=None):
    return render_to_response('admin/offline_messages.html', locals(), context_instance = RequestContext(request))

@admin_login
def message(request):
    return render_to_response('admin/message.html', locals(), context_instance = RequestContext(request))