from django.shortcuts import render_to_response, RequestContext
from django.db.models import Q

from vcg.utilities import caregiver_login
from vcg.admin_management.models import Caregiver
from vcg.company_management.models import CompanyClientPlan, CompanyClientTest, CompanyClientAssignment, CompanyClientDiary, CompanyClientTreatment, ClientTreatmentSessions, CompanyClientAnimation, CompanyForms

@caregiver_login
def caregiver_tasks(request, domain_name = None):
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)
    new_plan_list                       =  CompanyClientPlan.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_plan_list                  =  CompanyClientPlan.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_plan_list                      =  CompanyClientPlan.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True).order_by('-modified_at')
#    post_plan_read_list                 =  CompanyClientPlan.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_plan_list and not non_post_plan_list and not post_plan_list:
        none_plan = True

    new_test_list                       =  CompanyClientTest.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_test_list                  =  CompanyClientTest.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_test_list                      =  CompanyClientTest.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True).order_by('-modified_at')
#    post_test_read_list                 =  CompanyClientTest.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_test_list and not non_post_test_list and not post_test_list:
        none_test = True
        
    new_diary_list                      =  CompanyClientDiary.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_diary_list                 =  CompanyClientDiary.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_diary_list                     =  CompanyClientDiary.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True).order_by('-modified_at')
#    post_diary_read_list                =  CompanyClientDiary.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_diary_list and not non_post_diary_list and not post_diary_list:
        none_diary = True
        
    new_assignment_list                 =  CompanyClientAssignment.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_assignment_list            =  CompanyClientAssignment.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_assignment_list                =  CompanyClientAssignment.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True).order_by('-modified_at')
#    post_assignment_read_list           =  CompanyClientAssignment.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_assignment_list and not non_post_assignment_list and not post_assignment_list:
        none_assignment = True
        
    activated_treatment_modules         = ClientTreatmentSessions.objects.filter(Q(created_by = request.user) | Q(client_treatment__caregiver = caregiver), active = True, assign_status = True, activate_session = True, post_status = False).order_by('-modified_at')
    opened_treatment_modules            = ClientTreatmentSessions.objects.filter(Q(created_by = request.user) | Q(client_treatment__caregiver = caregiver), active = True, assign_status = False, activate_session = True, post_status = False).order_by('-modified_at')
    completed_treatment_modules         = ClientTreatmentSessions.objects.filter(Q(created_by = request.user) | Q(client_treatment__caregiver = caregiver), active = True, assign_status = False, activate_session = True, post_status = True).order_by('-modified_at')
#    post_treatment_read_list            = ClientTreatmentSessions.objects.filter(Q(created_by = request.user) | Q(client_treatment__caregiver = caregiver), active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not activated_treatment_modules and not opened_treatment_modules and not completed_treatment_modules:
        none_modules = True
        
    activated_treatment_questions       = CompanyClientTreatment.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, question_active_status = True, question_post_status = False).order_by('-modified_at')
    opened_treatment_questions          = CompanyClientTreatment.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, question_active_status = False, question_post_status = False).order_by('-modified_at')
    completed_treatment_questions       = CompanyClientTreatment.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, question_active_status = False, question_post_status = True).order_by('-modified_at')
#    completed_treatment_read_questions  = CompanyClientTreatment.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, question_active_status = False, question_post_status = True, question_post_read_status = True).order_by('-modified_at')
    if not activated_treatment_questions and not opened_treatment_questions and not completed_treatment_questions:
        none_questions = True

    new_animation_list                       =  CompanyClientAnimation.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = True, post_status = False).order_by('-modified_at')
    non_post_animation_list                  =  CompanyClientAnimation.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = False).order_by('-modified_at')
    post_animation_list                      =  CompanyClientAnimation.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True).order_by('-modified_at')
#    post_animation_read_list                      =  CompanyClientAnimation.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), active = True, assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_animation_list and not non_post_animation_list and not post_animation_list:
        none_animation = True

    new_forms_list                       =  CompanyForms.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), assign_status = True, post_status = False).order_by('-modified_at')
    non_post_forms_list                  =  CompanyForms.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), assign_status = False, post_status = False).order_by('-modified_at')
    post_forms_list                      =  CompanyForms.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), assign_status = False, post_status = True).order_by('-modified_at')
#    post_forms_read_list                      =  CompanyForms.objects.filter(Q(created_by = request.user) | Q(caregiver = caregiver), assign_status = False, post_status = True, post_read_status = True).order_by('-modified_at')
    if not new_forms_list and not non_post_forms_list and not post_forms_list:
        none_forms = True
        
    return render_to_response('caregiver/caregiver_tasks.html', locals(), context_instance=RequestContext(request))
