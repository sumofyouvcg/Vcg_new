from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Caregiver, Client, AssignmentCluster, AssignmentQuestion, AssignmentQuestionAnswer
from vcg.company_management.models import ClientCaregivers, CompanyClientAssignment, Messages
from vcg.company_management.client_assignment_forms import CompanyClientAssignmentForm
from vcg.client_management.models import ClientAssignment, AssignmentFeedback
from vcg.client_management.client_assignment_forms import AssignmentFeedbackForm
from vcg.utilities import company_login
from vcg.config import choices

@company_login
def client_assignment_list(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    assignment_list = CompanyClientAssignment.objects.filter(client__id = client_id).order_by('-modified_at')
    
    paginate  = Paginator(assignment_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        assignment_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        assignment_list = paginate.page(paginate.num_pages)
    num_pages = range(assignment_list.paginator.num_pages)
    return render_to_response('company/client_assignment_list.html', locals(), context_instance=RequestContext(request))

@company_login
def client_assignment_details(request, domain_name = None, client_id = None, assign_id = None):
    CompanyClientAssignment.objects.filter(id = assign_id).update(post_read_status = False)
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        assignment = CompanyClientAssignment.objects.get(pk = assign_id)
        selected_assignment = get_object_or_404(CompanyClientAssignment, pk = assign_id)
        all_actions = ClientAssignment.objects.filter(assignment = selected_assignment)
        exist_feedback = AssignmentFeedback.objects.filter(assignment = assign_id).order_by('created_at')
        assignments = ClientAssignment.objects.filter(assignment = selected_assignment)
        if request.method == "POST":
            form = AssignmentFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientAssignment.objects.filter(client__id = client_id, pk = assign_id, active = True).update(assign_status = True, post_status = False)
                
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('company_client_assignment_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('company/client_assignment_details.html', locals(), context_instance = RequestContext(request))
    
        form = AssignmentFeedbackForm()
    except CompanyClientAssignment.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_assignment_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
    return render_to_response('company/client_assignment_details.html', locals(), context_instance=RequestContext(request))

@company_login
def client_assignment_add(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    client = Client.objects.get(id = client_id)
    form    = CompanyClientAssignmentForm(user=request.user, initial={'client': client})
    if request.POST:
        form = CompanyClientAssignmentForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            assign = form.save(commit = False)
            assign.assign_status = True
            assign.created_by = assign.modified_by = request.user
            assign.save()
            ClientCaregivers.objects.create(client = assign.client , caregiver = assign.caregiver, task_id = "assign_"+str(assign.id), created_by = request.user, modified_by = request.user)
            messages.success(request,(_("Assignment  Assigned Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_client_assignment_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
        else:
            return render_to_response('company/client_assignment_add.html', locals(), context_instance = RequestContext(request))
    else:
        form    = CompanyClientAssignmentForm(user=request.user, initial={'client': client_id})
    return render_to_response('company/client_assignment_add.html', locals(), context_instance=RequestContext(request))

@company_login
def client_assignment_view(request, domain_name = None, client_id = None, assign_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        assignment = CompanyClientAssignment.objects.get(pk = assign_id)
        selected_assignment = get_object_or_404(CompanyClientAssignment, pk = assign_id)
        assignment_questions = AssignmentCluster.objects.filter(assignment__id = selected_assignment.assignment.id)
        paginate  = Paginator(assignment_questions, choices.list_per_page)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
    
        try:
            assignment_questions = paginate.page(page)
        except (EmptyPage, InvalidPage):
            assignment_questions = paginate.page(paginate.num_pages)
        num_pages = range(assignment_questions.paginator.num_pages)
        return render_to_response('company/client_assignment_view.html', locals(), context_instance=RequestContext(request))
    except CompanyClientAssignment.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_assignment_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
    
@company_login
def client_assignment_edit(request, domain_name = None, client_id = None, assign_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        try_assignment = CompanyClientAssignment.objects.get(pk = assign_id)
        selected_test = get_object_or_404(CompanyClientAssignment, pk = assign_id)
        if request.POST:
            form = CompanyClientAssignmentForm(request.POST, request.FILES,instance = selected_test, user=request.user)
            if form.is_valid():
                assign = form.save(commit = False)
                assign.assign_status = True
                assign.created_by = assign.modified_by = request.user
                assign.save()
                ClientCaregivers.objects.filter(client = assign.client, task_id = "assign_"+str(assign.id)).delete()
                ClientCaregivers.objects.create(client = assign.client , caregiver = assign.caregiver, task_id = "assign_"+str(assign.id), created_by = request.user, modified_by = request.user)
                messages.success(request,(_("Assignment Edited Successfully")),fail_silently = True)
                return redirect(reverse('company_client_assignment_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))
            else:
                return render_to_response('company/client_assignment_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = CompanyClientAssignmentForm(user=request.user, instance = selected_test)
        return render_to_response('company/client_assignment_edit.html', locals(), context_instance=RequestContext(request))
    except CompanyClientAssignment.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_assignment_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_assignment_delete(request, domain_name = None, client_id = None):
    if request.method == 'POST':
        company_client_assignment_ids    = request.POST.getlist('choices')
        for company_client_assignment_id in company_client_assignment_ids:
            assignment = CompanyClientAssignment.objects.get(id = company_client_assignment_id)
            assignment.delete()
        if len(company_client_assignment_ids) > 1:
            messages.success(request,(_("Selected Assignments Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Assignment Deleted Successfully")),fail_silently = True)
    return redirect(reverse('company_client_assignment_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))

@company_login
def client_assignment_questions(request, domain_name = None, client_id = None, assign_id = None, cluster_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        assignment = CompanyClientAssignment.objects.get(pk = assign_id)
        selected_test = get_object_or_404(CompanyClientAssignment, pk = assign_id)
        cluster_name = AssignmentCluster.objects.get(id = cluster_id)
        assignment_questions = AssignmentQuestion.objects.filter(assignment_cluster = cluster_id)
        assignment_answers = AssignmentQuestionAnswer.objects.filter(assignment_question__assignment_cluster = cluster_id)
        paginate  = Paginator(assignment_questions, choices.list_per_page)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
    
        try:
            assignment_questions = paginate.page(page)
        except (EmptyPage, InvalidPage):
            assignment_questions = paginate.page(paginate.num_pages)
        num_pages = range(assignment_questions.paginator.num_pages)
        return render_to_response('company/client_assignment_questions.html', locals(), context_instance=RequestContext(request))
    except CompanyClientAssignment.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed by Admin')), fail_silently= True)
        return redirect(reverse('company_client_assignment_list', kwargs={'domain_name': domain_name, 'client_id':client_id }))