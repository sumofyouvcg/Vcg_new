from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.client_management.client_msg_forms import MessagesForm, SentMessagesForm
from vcg.company_management.models import Messages, SentMessages
from vcg.utilities import client_login
from vcg.config import choices

@client_login
def message_list(request, domain_name = None):
    message_list = Messages.objects.filter(recipient = request.user, delete_status = False).order_by('-modified_at')
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)

    paginate  = Paginator(message_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        message_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        message_list = paginate.page(paginate.num_pages)
    num_pages = range(message_list.paginator.num_pages)
    return render_to_response('client/message_list.html', locals(), context_instance=RequestContext(request))

@client_login
def sent_message_list(request, domain_name = None):
    message_list = SentMessages.objects.filter(created_by = request.user).order_by('-modified_at')
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)

    paginate  = Paginator(message_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        message_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        message_list = paginate.page(paginate.num_pages)
    num_pages = range(message_list.paginator.num_pages)
    return render_to_response('client/sent_message_list.html', locals(), context_instance=RequestContext(request))

@client_login
def trash_message_list(request, domain_name = None):
    message_list = Messages.objects.filter(recipient = request.user, delete_status = True).order_by('-modified_at')
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)

    paginate  = Paginator(message_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        message_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        message_list = paginate.page(paginate.num_pages)
    num_pages = range(message_list.paginator.num_pages)
    return render_to_response('client/trash_message_list.html', locals(), context_instance=RequestContext(request))

@client_login
def client_message(request, domain_name = None):
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    if request.method == "POST":
        form = MessagesForm(request.POST, request.FILES, user=request.user)
        form1 = SentMessagesForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            msg_forms = [form, form1]
            for msg_form in msg_forms:
                msg = msg_form.save(commit = False)
                msg.created_by = msg.modified_by = request.user
                msg.save()
            messages.success(request,(_("Your Message Sent Successfully")),fail_silently = True)
            return redirect(reverse('client_message_list', kwargs={'domain_name': domain_name}))
        else:
            return render_to_response('client/client_message.html', locals(), context_instance = RequestContext(request))
    else:
        form = MessagesForm(user=request.user) 
    return render_to_response('client/client_message.html', locals(), context_instance=RequestContext(request))


@client_login
def client_reply_message(request, domain_name = None, reply_id = None):
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    try:
        msg = Messages.objects.get(pk = reply_id)
        reply_message = get_object_or_404(Messages, pk = reply_id)
        if request.method == "POST":
            form = MessagesForm(request.POST, request.FILES, user=request.user)
            form1 = SentMessagesForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                msg_forms = [form, form1]
                for msg_form in msg_forms:
                    msg = msg_form.save(commit = False)
                    msg.created_by = msg.modified_by = request.user
                    msg.save()
                messages.success(request,(_("Your Message Sent Successfully")),fail_silently = True)
                return redirect(reverse('client_message_list', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('client/client_reply_message.html', locals(), context_instance = RequestContext(request))
        else:
            form = MessagesForm(user=request.user) 
        return render_to_response('client/client_reply_message.html', locals(), context_instance=RequestContext(request))
    except Messages.DoesNotExist:
        messages.success(request,(_('This Message has been removed')), fail_silently= True)
        return redirect(reverse('client_message_list', kwargs={'domain_name': domain_name}))
    
@client_login
def client_reply_trash_message(request, domain_name = None, reply_id = None):
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    try:
        msg = Messages.objects.get(pk = reply_id)
        reply_message = get_object_or_404(Messages, pk = reply_id)
        if request.method == "POST":
            form = MessagesForm(request.POST, request.FILES, user=request.user)
            form1 = SentMessagesForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                msg_forms = [form, form1]
                for msg_form in msg_forms:
                    msg = msg_form.save(commit = False)
                    msg.created_by = msg.modified_by = request.user
                    msg.save()
                messages.success(request,(_("Your Message Sent Successfully")),fail_silently = True)
                return redirect(reverse('client_trash_message_list', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('client/client_reply_trash_message.html', locals(), context_instance = RequestContext(request))
        else:
            form = MessagesForm(user=request.user) 
        return render_to_response('client/client_reply_trash_message.html', locals(), context_instance=RequestContext(request))
    except Messages.DoesNotExist:
        messages.success(request,(_('This Message has been removed')), fail_silently= True)
        return redirect(reverse('client_trash_message_list', kwargs={'domain_name': domain_name})) 
    
@client_login
def client_view_message(request, domain_name = None, msg_id = None):
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    try:
        msg = Messages.objects.get(id = msg_id)
        reply_message = get_object_or_404(Messages, pk = msg_id)
        Messages.objects.filter(pk = msg_id).update(read_status = True)
        return render_to_response('client/client_view_message.html', locals(), context_instance=RequestContext(request))
    except Messages.DoesNotExist:
        messages.success(request,(_('This Message has been removed')), fail_silently= True)
        return redirect(reverse('client_message_list', kwargs={'domain_name': domain_name}))

@client_login
def client_view_sent_message(request, domain_name = None, msg_id = None):
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    try:
        msg = SentMessages.objects.get(id = msg_id)
        reply_message = get_object_or_404(SentMessages, pk = msg_id)
        return render_to_response('client/client_view_sent_message.html', locals(), context_instance=RequestContext(request))
    except SentMessages.DoesNotExist:
        messages.success(request,(_('This Message has been removed')), fail_silently= True)
        return redirect(reverse('client_sent_message_list', kwargs={'domain_name': domain_name}))
        
@client_login
def client_view_trash_message(request, domain_name = None, msg_id = None):
    new_messages = Messages.objects.filter(recipient = request.user, read_status = False, delete_status = False)
    try:
        msg = Messages.objects.get(id = msg_id)
        reply_message = get_object_or_404(Messages, pk = msg_id)
        Messages.objects.filter(pk = msg_id).update(read_status = True)
        return render_to_response('client/client_view_trash_message.html', locals(), context_instance=RequestContext(request))
    except Messages.DoesNotExist:
        messages.success(request,(_('This Message has been removed')), fail_silently= True)
        return redirect(reverse('client_trash_message_list', kwargs={'domain_name': domain_name}))
    
@client_login
def message_delete(request, domain_name = None):
    if request.method == 'POST':
        message_ids    = request.POST.getlist('choices')
        for message_id in message_ids:
            Messages.objects.filter(id = message_id).update(delete_status = True)
        if len(message_ids) > 1:
            messages.success(request,(_("The Message has been moved to the Trash Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("The Messages has been moved to the Trash Successfully")),fail_silently = True)
    return redirect(reverse('client_message_list', kwargs={'domain_name': domain_name}))

@client_login
def sent_message_delete(request, domain_name = None):
    if request.method == 'POST':
        message_ids    = request.POST.getlist('choices')
        for message_id in message_ids:
            message = SentMessages.objects.get(id = message_id)
            message.delete()
        if len(message_ids) > 1:
            messages.success(request,(_("The Message has been Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("The Messages has been Deleted Successfully")),fail_silently = True)
    return redirect(reverse('client_sent_message_list', kwargs={'domain_name': domain_name}))

@client_login
def trash_message_delete(request, domain_name = None):
    if request.method == 'POST':
        message_ids    = request.POST.getlist('choices')
        for message_id in message_ids:
            message = Messages.objects.get(id = message_id)
            message.delete()
        if len(message_ids) > 1:
            messages.success(request,(_("The Message has been Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("The Messages has been Deleted Successfully")),fail_silently = True)
    return redirect(reverse('client_trash_message_list', kwargs={'domain_name': domain_name}))

@client_login
def client_move_to_inbox(request, domain_name = None):
    if request.method == 'POST':
        message_ids    = request.POST.getlist('choices')
        for message_id in message_ids:
            Messages.objects.filter(id = message_id).update(delete_status = False)
        if len(message_ids) > 1:
            messages.success(request,(_("The Message has been moved to the Inbox")),fail_silently = True)
        else:    
            messages.success(request,(_("The Messages has been moved to the Inbox")),fail_silently = True)
    return redirect(reverse('client_trash_message_list', kwargs={'domain_name': domain_name}))