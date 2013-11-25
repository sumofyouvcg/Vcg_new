from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.utilities import company_login
from vcg.admin_management.models import Client
from vcg.company_management.models import Messages
from vcg.company_management.message_forms import MessagesForm, SentMessagesForm
from vcg.config import choices

@company_login
def client_send_message(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    user_id = User.objects.get(username = client.client_number).id
    
    if request.method == "POST":
        form = MessagesForm(request.POST, request.FILES, user=request.user)
        form1 = SentMessagesForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            msg_forms = [form, form1]
            for msg_form in msg_forms:
                msg = msg_form.save(commit = False)
                msg.created_by = msg.modified_by = request.user
                msg.save()
            messages.success(request,(_("Your Message has been sent successfully")),fail_silently = True)
            return redirect(reverse('company_client_home', kwargs={'domain_name': domain_name, 'client_id':client_id }))
        else:
            return render_to_response('company/client_send_message.html', locals(), context_instance = RequestContext(request))
    else:
        form = MessagesForm(user = request.user) 
    return render_to_response('company/client_send_message.html', locals(), context_instance=RequestContext(request))

@company_login
def client_messages(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    client_user = User.objects.get(username = client.client_number)
    client_message_list = Messages.objects.filter(created_by = client_user, recipient = request.user).order_by('-modified_at')
    
    paginate  = Paginator(client_message_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        client_message_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        client_message_list = paginate.page(paginate.num_pages)
    num_pages = range(client_message_list.paginator.num_pages)  
        
    return render_to_response('company/client_messages.html', locals(), context_instance=RequestContext(request))

@company_login
def client_messages_delete(request, domain_name = None, client_id = None):
    if request.method == 'POST':
        message_ids    = request.POST.getlist('choices')
        for message_id in message_ids:
            message = Messages.objects.get(id = message_id)
            message.delete()
        if len(message_ids) > 1:
            messages.success(request,(_("Selected Messages Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Message Deleted Successfully")),fail_silently = True)
    return redirect(reverse('company_client_messages', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_view_message(request, domain_name = None, client_id = None, msg_id = None):
    try:
        view_msg = Messages.objects.get(id = msg_id)
        client = Client.objects.get(id = client_id)
        client_user = User.objects.get(username = client.client_number)
        Messages.objects.filter(id = msg_id).update(read_status = True)
        new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
        return render_to_response('company/client_view_message.html', locals(), context_instance=RequestContext(request))
    except Messages.DoesNotExist:
        messages.success(request,(_('This Message has been removed')), fail_silently= True)
        return redirect(reverse('company_client_messages', kwargs={'domain_name': domain_name, 'client_id':client_id }))
    
@company_login
def client_reply_message(request, domain_name = None, client_id = None, msg_id = None):
    try:
        msg = Messages.objects.get(id = msg_id)
        client = Client.objects.get(id = client_id)
        client_user = User.objects.get(username = client.client_number)
        new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
        if request.method == "POST":
            form = MessagesForm(request.POST, request.FILES, user = request.user)
            if form.is_valid():
                msg = form.save(commit = False)
                msg.created_by = msg.modified_by = request.user
                msg.save()
                messages.success(request,(_("Your Message has been sent successfully")),fail_silently = True)
                return redirect(reverse('company_client_messages', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('company/client_reply_message.html', locals(), context_instance = RequestContext(request))
        else:
            form = MessagesForm(user = request.user) 
            user_id = User.objects.get(username = client.client_number).id
            return render_to_response('company/client_reply_message.html', locals(), context_instance=RequestContext(request))
    except Messages.DoesNotExist:
        messages.success(request,(_('This Message has been removed')), fail_silently= True)
        return redirect(reverse('company_client_messages', kwargs={'domain_name': domain_name, 'client_id':client_id }))