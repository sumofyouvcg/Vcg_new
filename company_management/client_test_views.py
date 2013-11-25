from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Client, TestQuestion, TestRange, TestQuestionAnswers
from vcg.company_management.models import ClientCaregivers, CompanyClientTest, Messages
from vcg.company_management.client_test_forms import CompanyClientTestForm 
from vcg.client_management.models import ClientTestAnswers, ClientTestResult, TestFeedback
from vcg.client_management.client_test_forms import TestFeedbackForm
from vcg.utilities import company_login
from vcg.config import choices

@company_login
def client_test_list(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    test_list = CompanyClientTest.objects.filter(client__id = client_id).order_by('-modified_at')
    
    paginate  = Paginator(test_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        test_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        test_list = paginate.page(paginate.num_pages)
    num_pages = range(test_list.paginator.num_pages)
    return render_to_response('company/client_test_list.html', locals(), context_instance=RequestContext(request))

@company_login
def client_test_add(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    form    = CompanyClientTestForm(user=request.user, initial={'client': client})
    if request.POST:
        form = CompanyClientTestForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            test = form.save(commit = False)
            test.assign_status = True
            test.created_by = test.modified_by = request.user
            test.save()
            ClientCaregivers.objects.create(client = test.client , caregiver = test.caregiver, task_id = "test_"+str(test.id), created_by = request.user, modified_by = request.user)
            messages.success(request,(_("Test  Assigned Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_client_test_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))        
        else:
            return render_to_response('company/client_test_add.html', locals(), context_instance = RequestContext(request))
    else:
        form    = CompanyClientTestForm(user=request.user, initial={'client': client_id})
    return render_to_response('company/client_test_add.html', locals(), context_instance = RequestContext(request))

@company_login
def client_test_view(request, domain_name = None, client_id = None, test_id = None):
    CompanyClientTest.objects.filter(id = test_id).update(post_read_status = False)

    client       = Client.objects.get(id = client_id)
    client_user  = User.objects.get(username = client.client_number)
    new_messages = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    try:
        test           = CompanyClientTest.objects.get( pk = test_id)
        selected_test  = get_object_or_404(CompanyClientTest, pk = test_id)
        test_result    = ClientTestResult.objects.filter(test = selected_test)
        test_questions = TestQuestion.objects.filter(test__id = selected_test.test.id)
        test_answers   = TestQuestionAnswers.objects.filter(question__test__id = selected_test.test.id)
        ranges         = TestRange.objects.filter(test__id = selected_test.test.id)

        if test_result:
            exist_feedback = TestFeedback.objects.filter(test = test_id).order_by('created_at')
            questions      = ClientTestAnswers.objects.filter(test = selected_test)
            all_actions    = ClientTestResult.objects.filter(test = selected_test)
            answers        = test_answers    
            form           = TestFeedbackForm()
            return render_to_response('company/client_test_completed.html', locals(), context_instance=RequestContext(request))

        return render_to_response('company/client_test_view.html', locals(), context_instance=RequestContext(request))

    except CompanyClientTest.DoesNotExist:
        messages.success(request,(_('This Test has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_test_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_test_edit(request, domain_name = None, client_id = None, test_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        try_test = CompanyClientTest.objects.get( pk = test_id)
        selected_test = get_object_or_404(CompanyClientTest, pk = test_id)
        if request.POST:
            form = CompanyClientTestForm(request.POST, request.FILES,instance = selected_test, user=request.user)
            if form.is_valid():
                test = form.save(commit = False)
                test.assign_status = True
                test.created_by = test.modified_by = request.user
                test.save()
                ClientCaregivers.objects.filter(client = test.client, task_id = "test_"+str(test.id)).delete()
                ClientCaregivers.objects.create(client = test.client , caregiver = test.caregiver, task_id = "test_"+str(test.id), created_by = request.user, modified_by = request.user)
                messages.success(request,(_("Test Edited Successfully")),fail_silently = True)
                return redirect(reverse('company_client_test_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('company/client_test_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = CompanyClientTestForm(user=request.user, instance = selected_test)
        return render_to_response('company/client_test_edit.html', locals(), context_instance=RequestContext(request))
    except CompanyClientTest.DoesNotExist:
        messages.success(request,(_('This Test has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_test_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
        
@company_login
def client_test_delete(request, domain_name = None, client_id = None):
    if request.method == 'POST':
        company_client_test_ids    = request.POST.getlist('choices')
        for company_client_test_id in company_client_test_ids:
            test = CompanyClientTest.objects.get(id = company_client_test_id)
            test.delete()
        if len(company_client_test_ids) > 1:
            messages.success(request,(_("Selected Tests Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Test Deleted Successfully")),fail_silently = True)
    return redirect(reverse('company_client_test_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_test_feedback(request, domain_name = None, client_id = None, test_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        test = CompanyClientTest.objects.get( pk = test_id)
        selected_test = get_object_or_404(CompanyClientTest, pk = test_id)
        test_result = ClientTestResult.objects.filter(test = selected_test)
        test_questions = TestQuestion.objects.filter(test__id = selected_test.test.id)
        ranges         = TestRange.objects.filter(test__id = selected_test.test.id)
        if test_result:
            exist_feedback = TestFeedback.objects.filter(test = test_id).order_by('created_at')
            questions = ClientTestAnswers.objects.filter(test = selected_test)
            all_actions = ClientTestResult.objects.filter(test = selected_test)  
        if request.method == "POST":
            form = TestFeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientTest.objects.filter(client__id = client_id, pk = test_id, active = True).update(assign_status = True, post_status = False)
                 
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('company_client_test_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('company/client_test_completed.html', locals(), context_instance = RequestContext(request))
            form = TestFeedbackForm()     
        return render_to_response('company/client_test_completed.html', locals(), context_instance = RequestContext(request))
    except CompanyClientTest.DoesNotExist:
        messages.success(request,(_('This Test has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_test_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))