import re

from django.shortcuts import render_to_response, HttpResponse, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import simplejson
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Client, Session, CompanyModules, Caregiver, CreateQuestion, CreateQuestionChoice, CreateQuestionSlider
from vcg.company_management.client_treatment_forms import CompanyClientTreatmentForm, ClientTreatmentSessionsForm, ClientSessionsFeedbackForm
from vcg.company_management.models import CompanyClientTreatment, ClientTreatmentSessions, ClientSessionsFeedback, ClientCaregivers, Messages
from vcg.client_management.models import ClientQuestions, ClientQuestionsFeedback,ClientQuestionsAnswers
from vcg.client_management.client_question_forms import ClientQuestionsFeedbackForm
from vcg.utilities import caregiver_login, view_access, company_access
from vcg.config import choices

@caregiver_login
@view_access
def client_treatment_list(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False   
            
    treatment_list = CompanyClientTreatment.objects.filter(client__id = client_id).order_by('-modified_at')
    paginate  = Paginator(treatment_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        treatment_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        treatment_list = paginate.page(paginate.num_pages)
    num_pages = range(treatment_list.paginator.num_pages)
    return render_to_response('caregiver/client_treatment_list.html', locals(), context_instance=RequestContext(request))

@caregiver_login
@company_access
def client_treatment_add(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    if request.method == "POST":
        form = CompanyClientTreatmentForm(request.POST, user=request.user)
        if form.is_valid():
            company = form.save(commit = False)
            company.created_by = company.modified_by = request.user
            company.module_active_status = True
            company.question_active_status = True
            company.save()
            if company.guidance == '1':
                feedback = True
            else:
                feedback = False
            treatment_modules_list = Session.objects.filter(module = company.module)
            for lists in treatment_modules_list:
                ClientTreatmentSessions.objects.create(client_treatment = company, client = client, module = company.module, sessions = lists, active = True, created_by = request.user, modified_by = request.user, make_unaccompanied = feedback)
            total_sessions = ClientTreatmentSessions.objects.filter(client_treatment = company, module = company.module, client = client_id).order_by('created_at')
            if total_sessions:
                if company.first_session_activation:
                    ClientTreatmentSessions.objects.filter(client_treatment = company, module = company.module, client = client_id, sessions = total_sessions[0].sessions, completed = False).update(activate_session = True, assign_status = True)
                else:
                    ClientTreatmentSessions.objects.filter(client_treatment = company, module = company.module, client = client_id, sessions = total_sessions[0].sessions, completed = False).update(activate_session = False)
            ClientCaregivers.objects.create(client = company.client , caregiver = company.caregiver, task_id = "treat_"+str(company.id), created_by = request.user, modified_by = request.user)
            messages.success(request,(_("Treatment added Successfully")),
                                         fail_silently = True)
            return redirect(reverse('caregiver_client_treatment_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))
            
        else:
            return render_to_response('caregiver/client_treatment_add.html', locals(), context_instance = RequestContext(request))
    else:
        form = CompanyClientTreatmentForm(user=request.user)

        return render_to_response('caregiver/client_treatment_add.html', locals(), context_instance = RequestContext(request))

@caregiver_login
@view_access
def client_treatment_view(request, domain_name = None, client_id = None, module_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False
            
    active_session = request.GET.get('query')
    if active_session:
        session_act = ClientTreatmentSessions.objects.filter(client_treatment = module_id, client = client_id, sessions = active_session)
        session_act.update(activate_session = True, assign_status = True)
    completed_session = request.GET.get('complete')
    if completed_session:
        session_act = ClientTreatmentSessions.objects.filter(client_treatment = module_id, client = client_id, sessions = completed_session)
        session_act.update(completed = True)
    make_unaccompany = request.GET.get('make')
    if make_unaccompany:
        session_act = ClientTreatmentSessions.objects.filter(client_treatment = module_id, client = client_id, sessions = make_unaccompany)
        if session_act[0].make_unaccompanied:
            accompany = False
        else:
            accompany = True
        session_act.update(make_unaccompanied = accompany)
    try:    
        company_client = CompanyClientTreatment.objects.get(id = module_id, client = client_id)
        
        total_sessions = ClientTreatmentSessions.objects.filter(client_treatment = module_id, client = client_id).order_by('created_at')
        paginate  = Paginator(total_sessions, choices.list_per_page)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
    
        try:
            total_sessions = paginate.page(page)
        except (EmptyPage, InvalidPage):
            total_sessions = paginate.page(paginate.num_pages)
        num_pages = range(total_sessions.paginator.num_pages)
        
        client_questions = ClientQuestions.objects.filter(client = client, question__module__id = company_client.module.id)
        
        client_question_answer = ClientQuestionsAnswers.objects.filter(module = company_client, client = client)
        client_question_choices = ClientQuestionsAnswers.objects.filter(Q(answer_type = '2')|Q(answer_type = '3'),module = company_client, client = client)
        full_choices =[]
        if client_question_choices:
            for client_choice in client_question_choices:
                choice_options = client_choice.answer.splitlines()
                choice_value = []
                for options in choice_options:
                    if not re.match(r'^[\s]*$', options):
                        if not (options == ''):
                            choice_value.append(options)
                full_choices.append({'question':client_choice.client_question_id, 'options':choice_value})
                
        slider_val=[]
        choice_val=[]
        all_ques = CreateQuestion.objects.filter(module = company_client.module.id)
        if all_ques:
            for ques in all_ques:
                all_choice = CreateQuestionChoice.objects.filter(create_question__id = ques.id,)
                new_options=[]
                if all_choice:
                    for choice in all_choice:
                        options = choice.answer.splitlines()
                        new_options=[]
                        for option in options:
                            if not re.match(r'^[\s]*$', option):
                                if not (option == ''):
                                    new_options.append(option)
                
                    choice_val.append({'ques_id':choice.create_question.id,'answer':new_options})    
                all_slider = CreateQuestionSlider.objects.filter(create_question__id = ques.id)
                if all_slider:
                    for slider in all_slider:
                        slider_val.append({'ques_id':slider.create_question.id,'min_val':slider.min_value, 'max_val':slider.max_value})
        
        exist_feedback = ClientQuestionsFeedback.objects.filter(client = client_id, client_treatment = module_id).order_by('created_at')
        
        if request.method == "POST":
            form = ClientQuestionsFeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientTreatment.objects.filter(client__id = client_id, module = module_id, active = True).update(question_active_status = True, question_post_status = False)
                
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('caregiver_client_treatment_view', kwargs={'domain_name': domain_name, 'client_id':client_id, 'module_id':module_id}))
                
            else:
                return render_to_response('caregiver/client_treatment_view.html', locals(), context_instance = RequestContext(request))
        form = ClientQuestionsFeedbackForm()
    except CompanyClientTreatment.DoesNotExist:
        messages.success(request,(_('This treatment has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_treatment_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))
    return render_to_response('caregiver/client_treatment_view.html', locals(), context_instance=RequestContext(request))

@caregiver_login
@company_access
def client_treatment_edit(request, domain_name = None, client_id = None, company_id= None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        treat_ment = CompanyClientTreatment.objects.get(id = company_id, client = client_id)
        selected_company = get_object_or_404(CompanyClientTreatment, id = company_id, client = client_id)
        if request.method == "POST":
            form = CompanyClientTreatmentForm(request.POST, instance = selected_company, user=request.user)
            if form.is_valid():
                company = form.save(commit = False)
                company.created_by = company.modified_by = request.user
                company.save()
                if company.guidance == '1':
                    feedback = True
                else:
                    feedback = False
                treatment_modules_list = Session.objects.filter(module = company.module)
                for lists in treatment_modules_list:
                    client_details = Client.objects.get(id = client_id)
                    ClientTreatmentSessions.objects.filter(client_treatment = company, client = client_details, module = company.module, sessions = lists, active = True).update(make_unaccompanied = feedback)
                total_sessions = ClientTreatmentSessions.objects.filter(module = company.module, client = client_id).order_by('created_at')
                if total_sessions:
                    if company.first_session_activation:
                        ClientTreatmentSessions.objects.filter(client_treatment = company, module = company.module, client = client_id, sessions = total_sessions[0].sessions, completed = False).update(activate_session = True, assign_status = True)
                    else:
                        ClientTreatmentSessions.objects.filter(client_treatment = company, module = company.module, client = client_id, sessions = total_sessions[0].sessions, completed = False).update(activate_session = False)
                        
                ClientTreatmentSessions.objects.filter(client_treatment = company, module = company.module, client = client_id, activate_session = True, completed = False).update(assign_status = True)
                
                ClientCaregivers.objects.filter(client = client_id ,task_id = "treat_"+str(company.id)).delete()
                ClientCaregivers.objects.create(client = company.client , caregiver = company.caregiver, task_id = "treat_"+str(company.id), created_by = request.user, modified_by = request.user)
                messages.success(request,(_("Treatment Edited Successfully")),
                                             fail_silently = True)
                return redirect(reverse('caregiver_client_treatment_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))
            else:
                return render_to_response('caregiver/client_treatment_edit.html', locals(), context_instance = RequestContext(request))
        else:
            form = CompanyClientTreatmentForm(user=request.user, instance = selected_company)
            return render_to_response('caregiver/client_treatment_edit.html', locals(), context_instance = RequestContext(request))
    except CompanyClientTreatment.DoesNotExist:
        messages.success(request,(_('This treatment has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_treatment_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))
    
@caregiver_login
@company_access
def client_treatment_custom(request, domain_name = None, client_id = None, module_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    try:
        company_client = CompanyClientTreatment.objects.get(id = module_id, client = client_id)
        if request.method == "POST":
            form = ClientTreatmentSessionsForm(request.POST, user=request.user)
            if form.is_valid():
                custom = form.save(commit = False)
                custom.module = company_client.module
                custom.created_by = custom.modified_by = request.user
                custom.active = True
                custom.make_unaccompanied = True
                custom.save()
                messages.success(request,(_("Treatment Customized Successfully")),
                                             fail_silently = True)
                return redirect(reverse('caregiver_client_treatment_view', kwargs={'domain_name': domain_name, 'client_id':client_id, 'module_id':module_id}))
            else:
                return render_to_response('caregiver/client_treatment_custom.html', locals(), context_instance = RequestContext(request))
        else:
            form = ClientTreatmentSessionsForm(user=request.user)
            return render_to_response('caregiver/client_treatment_custom.html', locals(), context_instance = RequestContext(request))
    except CompanyClientTreatment.DoesNotExist:
        messages.success(request,(_('This Treatment has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_treatment_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))
    
@caregiver_login
@view_access
def client_treatment_session(request, domain_name = None, client_id = None, session_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False
    try:
        session = ClientTreatmentSessions.objects.get(id = session_id, client = client_id)
        
        exist_feedback = ClientSessionsFeedback.objects.filter(treatment_session = session_id, client = client_id).order_by('created_at')
        if request.method == "POST":
            form = ClientSessionsFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                ClientTreatmentSessions.objects.filter(client__id = client_id, pk = session_id, active = True).update(assign_status = True, post_status = False)
                #CompanyClientTreatment.objects.filter(client__id = client_id, id = session.client_treatment.id, active = True).update(module_active_status = True, module_post_status = False)
                
                messages.success(request,(_("Reply Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('caregiver_client_treatment_view', kwargs={'domain_name': domain_name, 'client_id':client_id, 'module_id':str(session.client_treatment.id)}))
            else:
                return render_to_response('caregiver/client_treatment_session.html', locals(), context_instance = RequestContext(request))
        else:
            form = ClientSessionsFeedbackForm()
    except ClientTreatmentSessions.DoesNotExist:
        messages.success(request,(_('This session has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_treatment_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))
    return render_to_response('caregiver/client_treatment_session.html', locals(), context_instance = RequestContext(request))

@caregiver_login
@company_access
def client_session_delete(request, domain_name = None, client_id = None, session_id = None):
    module_name = ClientTreatmentSessions.objects.get(id = session_id)
    ClientTreatmentSessions.objects.filter(client = client_id, id = session_id).delete()
    return redirect(reverse('caregiver_client_treatment_view', kwargs={'domain_name': domain_name, 'client_id':client_id,'module_id':str(module_name.client_treatment.id)}))

@caregiver_login
@company_access
def client_session_choices(request, domain_name = None, module_id = None, client_id = None, treat_mod_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    session_list = []
    current_lists =[]
    
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)
    treatment_module = CompanyModules.objects.get(modules = module_id, company__company_number = caregiver.company.company_number)
    
    sessions = Session.objects.filter(module = treatment_module.modules)
    present_session = ClientTreatmentSessions.objects.filter(client = client_id, client_treatment = treat_mod_id)
    
    for lists in present_session:
        current_lists.append(lists.sessions.id)
    for each_session in sessions:
        if not each_session.id in current_lists:
            [session_list.append((each_session.pk,each_session.name)) ]
    if not session_list:
        [session_list.append(('','No Sessions to Customize'))]
    json = simplejson.dumps(session_list)
    return HttpResponse(json, mimetype = "application/javascript")

@caregiver_login
@company_access
def client_treatment_delete(request, domain_name = None, client_id = None):
    if request.method == 'POST':
        company_client_treatment_ids    = request.POST.getlist('choices')
        for company_client_treatment_id in company_client_treatment_ids:
            treatment = CompanyClientTreatment.objects.get(id = company_client_treatment_id)
            treatment.delete()
        if len(company_client_treatment_ids) > 1:
            messages.success(request,(_("Selected Treatments Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Treatment Deleted Successfully")),fail_silently = True)
    return redirect(reverse('caregiver_client_treatment_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))