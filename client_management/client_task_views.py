from django.shortcuts import render_to_response
from django.template import RequestContext

from vcg.company_management.models import CompanyClientPlan, CompanyClientTest, CompanyClientAssignment, CompanyClientDiary, CompanyClientTreatment, ClientTreatmentSessions, CompanyClientAnimation, CompanyForms
from vcg.utilities import client_login

@client_login
def task_list(request, domain_name = None):  
    new_plan_list       =  CompanyClientPlan.objects.filter(client__client_number = request.user.username, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_plan_list  =  CompanyClientPlan.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_plan_list      =  CompanyClientPlan.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    if not new_plan_list and not non_post_plan_list and not post_plan_list:
        none_plan = True

    new_test_list       =  CompanyClientTest.objects.filter(client__client_number = request.user.username, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_test_list  =  CompanyClientTest.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_test_list      =  CompanyClientTest.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    if not new_test_list and not non_post_test_list and not post_test_list:
        none_test = True
        
    new_diary_list       =  CompanyClientDiary.objects.filter(client__client_number = request.user.username, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_diary_list  =  CompanyClientDiary.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_diary_list      =  CompanyClientDiary.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    if not new_diary_list and not non_post_diary_list and not post_diary_list:
        none_diary = True
        
    new_assignment_list      =  CompanyClientAssignment.objects.filter(client__client_number = request.user.username, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_assignment_list =  CompanyClientAssignment.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_assignment_list     =  CompanyClientAssignment.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    if not new_assignment_list and not non_post_assignment_list and not post_assignment_list:
        none_assignment = True
    
    
    activated_treatment_modules = ClientTreatmentSessions.objects.filter(client__client_number = request.user.username, active = True, activate_session = True, assign_status = True, post_status = False).order_by('-modified_at')
    completed_treatment_modules = ClientTreatmentSessions.objects.filter(client__client_number = request.user.username, active = True, activate_session = True, assign_status = False, post_status = True).order_by('-modified_at')
    opened_treatment_modules    = ClientTreatmentSessions.objects.filter(client__client_number = request.user.username, active = True, activate_session = True, assign_status = False, post_status = False).order_by('-modified_at')
    if not activated_treatment_modules and not opened_treatment_modules and not completed_treatment_modules:
        none_modules = True
        
    activated_treatment_questions   = CompanyClientTreatment.objects.filter(client__client_number = request.user.username, active = True, question_active_status = True, question_post_status = False).order_by('-modified_at')
    completed_treatment_questions   = CompanyClientTreatment.objects.filter(client__client_number = request.user.username, active = True, question_active_status = False, question_post_status = True).order_by('-modified_at')
    opened_treatment_questions      = CompanyClientTreatment.objects.filter(client__client_number = request.user.username, active = True, question_active_status = False, question_post_status = False).order_by('-modified_at')
    if not activated_treatment_questions and not opened_treatment_questions and not completed_treatment_questions:
        none_questions = True
        
    new_animation_list      =  CompanyClientAnimation.objects.filter(client__client_number = request.user.username, active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_animation_list =  CompanyClientAnimation.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_animation_list     =  CompanyClientAnimation.objects.filter(client__client_number = request.user.username, active = True, assign_status = False, post_status = True).order_by('-modified_at')
    if not new_animation_list and not non_post_animation_list and not post_animation_list:
        none_animation = True
    
    new_forms_list      =  CompanyForms.objects.filter(client__client_number = request.user.username, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_forms_list =  CompanyForms.objects.filter(client__client_number = request.user.username, assign_status = False, post_status = False).order_by('-modified_at')
    post_forms_list     =  CompanyForms.objects.filter(client__client_number = request.user.username, assign_status = False, post_status = True).order_by('-modified_at')
    if not new_forms_list and not non_post_forms_list and not post_forms_list:
        none_forms = True
        
    return render_to_response('client/client_task_list.html', locals(), context_instance = RequestContext(request))
