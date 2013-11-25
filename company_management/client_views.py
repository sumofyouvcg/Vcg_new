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

from vcg.admin_management.client_forms import ClientForm
from vcg.admin_management.models import Client, Company
from vcg.utilities import Utility, Email, company_login
from vcg.config import default_groups, mail
from vcg.company_management.models import CompanyClientPlan, CompanyClientTest, CompanyClientAssignment, CompanyClientDiary, CompanyClientTreatment, Messages, ClientTreatmentSessions, CompanyClientAnimation, CompanyForms
from vcg.client_management.models import ChatMessage
from vcg.config import choices

@company_login
def client_home(request, domain_name = None, client_id = None):
    client          = Client.objects.get(id = client_id)
    client_user     = User.objects.get(username = client.client_number)
    new_messages    = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    new_plan_list                       =  CompanyClientPlan.objects.filter(client__id = client_id, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_plan_list                  =  CompanyClientPlan.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_plan_list                      =  CompanyClientPlan.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    post_plan_read_list                 =  CompanyClientPlan.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_plan_list and not non_post_plan_list and not post_plan_list:
        none_plan = True

    new_test_list                       =  CompanyClientTest.objects.filter(client__id = client_id, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_test_list                  =  CompanyClientTest.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_test_list                      =  CompanyClientTest.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    post_test_read_list                 =  CompanyClientTest.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_test_list and not non_post_test_list and not post_test_list:
        none_test = True
        
    new_diary_list                      =  CompanyClientDiary.objects.filter(client__id = client_id, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_diary_list                 =  CompanyClientDiary.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_diary_list                     =  CompanyClientDiary.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    post_diary_read_list                =  CompanyClientDiary.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_diary_list and not non_post_diary_list and not post_diary_list:
        none_diary = True
        
    new_assignment_list                 =  CompanyClientAssignment.objects.filter(client__id = client_id, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_assignment_list            =  CompanyClientAssignment.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_assignment_list                =  CompanyClientAssignment.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    post_assignment_read_list           =  CompanyClientAssignment.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')    
    if not new_assignment_list and not non_post_assignment_list and not post_assignment_list:
        none_assignment = True
        
    activated_treatment_modules         = ClientTreatmentSessions.objects.filter(client__id = client_id, active = True, activate_session = True, assign_status = True, post_status = False).order_by('-modified_at')
    completed_treatment_modules         = ClientTreatmentSessions.objects.filter(client__id = client_id, active = True, activate_session = True, assign_status = False, post_status = True).order_by('-modified_at')
    opened_treatment_modules            = ClientTreatmentSessions.objects.filter(client__id = client_id, active = True, activate_session = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_treatment_read_list            = ClientTreatmentSessions.objects.filter(client__id = client_id, active = True, activate_session = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not activated_treatment_modules and not opened_treatment_modules and not completed_treatment_modules:
        none_modules = True
        
    activated_treatment_questions       = CompanyClientTreatment.objects.filter(client__id = client_id, active = True, question_active_status = True, question_post_status = False).order_by('-modified_at')
    completed_treatment_questions       = CompanyClientTreatment.objects.filter(client__id = client_id, active = True, question_active_status = False, question_post_status = True).order_by('-modified_at')
    opened_treatment_questions          = CompanyClientTreatment.objects.filter(client__id = client_id, active = True, question_active_status = False, question_post_status = False).order_by('-modified_at')
    completed_treatment_read_questions  = CompanyClientTreatment.objects.filter(client__id = client_id, active = True, question_active_status = False, question_post_status = True, question_post_read_status = True).order_by('-modified_at')    
    if not activated_treatment_questions and not opened_treatment_questions and not completed_treatment_questions:
        none_questions = True

    new_animation_list                  =  CompanyClientAnimation.objects.filter(client__id = client_id, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_animation_list             =  CompanyClientAnimation.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_animation_list                 =  CompanyClientAnimation.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    post_animation_read_list            =  CompanyClientAnimation.objects.filter(client__id = client_id, active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_animation_list and not non_post_animation_list and not post_animation_list:
        none_animation = True

    new_forms_list                  =  CompanyForms.objects.filter(client__id = client_id, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_forms_list             =  CompanyForms.objects.filter(client__id = client_id, assign_status = False, post_status = False).order_by('-modified_at')
    post_forms_list                 =  CompanyForms.objects.filter(client__id = client_id, assign_status = False, post_status = True).order_by('-modified_at')
    post_forms_read_list            =  CompanyForms.objects.filter(client__id = client_id, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_forms_list and not non_post_forms_list and not post_forms_list:
        none_forms = True
        
    return render_to_response('company/client_home.html', locals(), context_instance=RequestContext(request))

@company_login
def client_list(request, domain_name = None):
    
    if request.user.id:
        company_number = request.user.username
        company_id = Company.objects.get(company_number = company_number).id
    key = request.GET.get('keyword')
    filter_val = request.GET.get('filter')
    
    if filter_val:
        if filter_val=="InActive":
            client_list = Client.objects.filter(active = False, company = company_id).order_by('-modified_at')
        elif filter_val == "Active":    
            client_list = Client.objects.filter(active = True, company = company_id).order_by('-modified_at')
    if key is not None: 
        key = key.lstrip()
    if key :
        client_list = Client.objects.filter(Q(name__icontains = key)|Q(place_name__icontains = key)|Q(zip_code__icontains = key)|Q(address__icontains = key)|Q(phone_number = key)|Q(client_number__icontains = key)|Q(email__icontains = key), company = company_id).order_by('-modified_at')
    if not filter_val and not key:
        client_list = Client.objects.filter(company = company_id).order_by('-modified_at')
    
    paginate  = Paginator(client_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        client_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        client_list = paginate.page(paginate.num_pages)
    num_pages = range(client_list.paginator.num_pages)  
    
    return render_to_response('company/client_list.html', locals(), context_instance=RequestContext(request))

@company_login
def client_add(request, domain_name = None, company_id = None):
    comp = Company.objects.get(id = company_id)
    form    = ClientForm( initial={'company': comp})
    if request.POST:
        form = ClientForm(request.POST, request.FILES, initial={'company': comp})
        if form.is_valid():
            no_of_client     = Client.objects.filter(company = comp)
            if len(no_of_client) >= comp.number_of_clients:
                messages.success(request,(_("You are Authorized to add %s Clients Only") % str(comp.number_of_clients)), fail_silently = True)
                return redirect(reverse('company_client_list', kwargs={'domain_name': domain_name}))
            client = form.save(commit = False)
            client.created_by = client.modified_by = request.user
            client.save()
            # For User Mgnt            
            random_password = Utility().generate_password()
            auth_user = User.objects.create_user(client.client_number, client.email, random_password)
            auth_user.is_active = True
            auth_user.is_staff = True
            auth_user.first_name = client.name
            default_groups.CLIENT = Group.objects.get(pk = 4)
            auth_user.groups = list(auth_user.groups.all()) + [default_groups.CLIENT, ]
            auth_user.save()
            Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_CREATION_MSG %(client.name, client.company.sub_domain, client.client_number, random_password), [client.email], "html")
            messages.success(request,(_("client Saved Successfully")),
                                         fail_silently = True)
            return redirect(reverse('company_client_list', kwargs={'domain_name': domain_name}))
        else:
            return render_to_response('company/client_add.html', locals(), context_instance=RequestContext(request))
    else:
        form = ClientForm(initial={'company': company_id})
    return render_to_response('company/client_add.html', locals(), context_instance=RequestContext(request))

@company_login
def client_details(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    selected_client = get_object_or_404(Client, pk = client_id)
    old_email = selected_client.email
    if request.POST:
        form = ClientForm(request.POST, request.FILES,instance = selected_client)
        if form.is_valid():
            client = form.save(commit = False)
            client.created_by = client.modified_by = request.user
            if not form.files:
                client.client_image = ''
            client.save()
            User.objects.filter(username = client.client_number).update(first_name = client.name)
            if old_email != client.email:
                User.objects.filter(email = old_email).update(username = client.client_number, email = client.email)
                Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_EDIT_MSG %(client.name, client.company.sub_domain, client.client_number), [client.email], "html")
            messages.success(request,(_("Client Edited Successfully")),fail_silently = True)
            return redirect(reverse('company_client_home', kwargs={'domain_name': domain_name, 'client_id': client_id}))
        else:
            return render_to_response('company/client_details.html', locals(), context_instance=RequestContext(request))
    else:
        form = ClientForm(instance = selected_client)
    return render_to_response('company/client_details.html', locals(), context_instance=RequestContext(request))


@company_login
def client_moniter_list(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    return render_to_response('company/client_moniter_list.html', locals(), context_instance=RequestContext(request))

@company_login
def client_caregiver_chat(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    return render_to_response('company/client_caregiver_chat.html', locals(), context_instance = RequestContext(request))

@company_login
def client_caregiver_video(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))

    return render_to_response('company/client_caregiver_video.html', locals(), context_instance = RequestContext(request))

@company_login
def video_details(request, domain_name = None, client_id = None):
    return render_to_response('company/video_details.html', locals(), context_instance = RequestContext(request))    