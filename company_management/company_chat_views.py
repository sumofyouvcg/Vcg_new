import datetime
import time

from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.db.models import Q

from vcg.client_management.models import ChatMessage, LastActive
from vcg.admin_management.models import Company, Caregiver, Client
from vcg.company_management.models import Messages
from vcg.utilities import company_login
from vcg.config import choices

@csrf_exempt
def chat_user(request, domain_name = None):
    username = request.user
    state=''
    return render_to_response('company/company_chat.html', locals(), context_instance=RequestContext(request))


@csrf_exempt
def post(request, domain_name = None):
    time.sleep(2)
    if not request.is_ajax():
        HttpResponse ("Not an AJAX request")
    if request.method == 'POST':
        if request.POST['message']:
            message = request.POST['message']
            to_user = request.POST['to_user']
            #ChatMessage.objects.create(sender = request.user, receiver = User.objects.get(username = to_user), message = message,  session = Session.objects.get(session_key = request.session.session_key))
            ChatMessage.objects.create(sender = request.user, receiver = User.objects.get(username = to_user), message = message)
    return HttpResponse (" Not an POST request ")


@csrf_exempt


def find_online_users(username, domain_name = None):
    print "user-------------------------------------",username
    if Company.objects.filter(company_number__icontains = username):
        print "company--------------------------", Company.objects.filter(company_number__icontains = username)
    last_active_list = LastActive.objects.filter(received_at__lt = datetime.datetime.now() - datetime.timedelta(seconds=5))
    print last_active_list
    users_list = []
    for last_active in last_active_list:
        users_list.append(last_active.user.username)    
    #users_list.remove(username)
    return ",".join(users_list)


def get(request, domain_name = None):
    print "=" * 50
    
    print request.session.session_key
    #print request
    print "=" * 50
    if not request.is_ajax():
        return  HttpResponse ("Not an AJAX request")  
    if request.method == 'GET':
        
        
        last_active = None
        try:
            last_active = LastActive.objects.get(user = request.user)
            last_active.session = Session.objects.get(session_key = request.session.session_key)
            last_active.save()
        except:
            last_active = LastActive.objects.create(user = request.user, session = Session.objects.get(session_key = request.session.session_key))        
        last_active.save()
        
        chat_list_today = ChatMessage.objects.filter(Q(sender=request.user)|Q(receiver = request.user), received_at__gte=datetime.date.today(), is_read = True).order_by('received_at')
        #session = Session.objects.get(session_key = request.session.session_key)        
        str_html = ''
        for chat in chat_list_today:  
            str_html += chat.sender.username    
            str_html += "^-#"
            str_html += chat.message
            str_html += "|,|"

        chat_list = ChatMessage.objects.filter(receiver = request.user, is_read = False)
        for chat in chat_list:
            chat.is_read = True
            print chat.is_read
            chat.save()
            print chat.is_read          
            
            return HttpResponse (chat.sender.username + "%:$" + chat.message + "%:$" + str_html, "html")
    print "========= After Scaling ==============="
    if Company.objects.filter(company_number = request.user.username):
        print "company--------------------------", Company.objects.filter(company_number = request.user.username)
        authorized_caregivers = Caregiver.objects.filter(company__company_number = request.user.username)
        auth_care = []
        for a in authorized_caregivers:
            auth_care.append(a.caregiver_number)
        authorized_clients = Client.objects.filter(company__company_number = request.user.username)
        for b in authorized_clients:
            auth_care.append(b.client_number) 
            
    #last_active_list=LastActive.objects.filter( received_at__gt = datetime.datetime.now() - datetime.timedelta(seconds=19090))
    last_active_list = LastActive.objects.filter(user__username__in = auth_care, received_at__gt = datetime.datetime.now() - datetime.timedelta(seconds=29090))
    users_list = []
    for last_active in last_active_list:
        users_list.append(last_active.user.username)
    if request.user.username in users_list:    
        users_list.remove(request.user.username)
    q= ",".join(users_list)

    return HttpResponse(str_html + 'ACTIVE:' + q)

@company_login
def chat_old_details(request, domain_name = None, username = None):
    chat_list_today = ChatMessage.objects.filter(Q(sender=request.user, receiver__username = username)|Q(receiver = request.user, sender__username=username), received_at__gte=datetime.date.today(), is_read = True).order_by('received_at')
    #session = Session.objects.get(session_key = request.session.session_key)        
    str_html = ''
    for chat in chat_list_today:  
        str_html += chat.sender.username    
        str_html += "^-#"
        str_html += chat.message
        str_html += "|,|"
    return HttpResponse(str_html)

@company_login
def company_chat_details(request, domain_name = None):
    message_list = Messages.objects.filter(recipient = request.user, delete_status = False).order_by('-modified_at')
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    
    chat_messages = ChatMessage.objects.filter(Q(sender = request.user.id)|Q(receiver = request.user.id)).order_by('received_at')
    client_chat_history = chat_messages.extra({'received_at' : "date(received_at)"}).values('received_at').distinct()
    print "client_chat_history",len(client_chat_history)
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
    return render_to_response('company/company_chat_details.html', locals(), context_instance = RequestContext(request))

@company_login
def company_chat_persons(request, domain_name = None, date = None):
    message_list = Messages.objects.filter(recipient = request.user, delete_status = False).order_by('-modified_at')
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    
    chat_date = str(date)
    chat_messages = ChatMessage.objects.filter(Q(sender = request.user.id)|Q(receiver = request.user.id), received_at__startswith = str(date)).order_by('received_at')
    chat_person = []
    for chat in chat_messages:
        if request.user == chat.sender and chat.receiver.id not in chat_person:
            chat_person.append(chat.receiver.id)
        elif request.user == chat.receiver and chat.sender.id not in chat_person:
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
    return render_to_response('company/company_chat_persons.html', locals(), context_instance = RequestContext(request))

@company_login
def company_chat_history(request, domain_name = None, date = None, user_id = None):
    message_list = Messages.objects.filter(recipient = request.user, delete_status = False).order_by('-modified_at')
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    
    chat_user = User.objects.get(id = user_id)
    chat_messages = ChatMessage.objects.filter(Q(sender = request.user.id, receiver = user_id )|Q(receiver = request.user.id, sender = user_id), received_at__startswith = str(date)).order_by('received_at')
    
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
    return render_to_response('company/company_chat_history.html', locals(), context_instance = RequestContext(request))