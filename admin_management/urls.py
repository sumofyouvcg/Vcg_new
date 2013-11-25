from django.conf.urls.defaults import patterns

urlpatterns = patterns('admin_management.company_views', 
                       (r'^company_add/(?P<comp_id>\d+)/$', 'company_add'),
                       (r'^company_add/', 'company_add'),
                       (r'^company_list/(?P<comp_id>\d+)/$','company_list'),
                       (r'^company_list/', 'company_list'),
                       (r'^company_edit/(?P<company_id>\d+)/$', 'company_edit'),
                       (r'^company_caregivers/(?P<company_id>\d+)/$','company_caregivers'),
                       (r'^company_client/(?P<company_id>\d+)/$','company_client'),
                       (r'^company_modules/(?P<comp_id>\d+)/$','company_modules'),
                       (r'^company_modules/','company_modules'),
                       (r'^company_delete/','company_delete'),
                       (r'^company_add_caregiver/(?P<company_id>\d+)/$','company_add_caregiver'),
                       (r'^company_add_client/(?P<company_id>\d+)/$','company_add_client'),
                       (r'^company_add_modules/(?P<company_id>\d+)/$','company_add_modules'),
                       (r'^company_edit_caregiver/(?P<company_id>\d+)/(?P<caregiver_id>\d+)/$','company_edit_caregiver'),
                       (r'^company_delete_caregiver/(?P<company_id>\d+)/$','company_delete_caregiver'),
                       (r'^company_edit_client/(?P<company_id>\d+)/(?P<client_id>\d+)/$','company_edit_client'),
                       (r'^company_delete_client/(?P<company_id>\d+)/$','company_delete_client'),
                       )

urlpatterns += patterns('admin_management.caregivers_views', 
                       (r'^caregivers_add/(?P<comp_id>\d+)/$', 'caregivers_add'),
                       (r'^caregivers_add/', 'caregivers_add'),
                       (r'^caregivers_edit/(?P<caregiver_id>\d+)/$', 'caregivers_edit'),
                       (r'^caregivers_list/', 'caregivers_list'),
                       (r'^caregivers_delete/', 'caregivers_delete'),
                       (r'^caregiver_client/(?P<caregiver_id>\d+)/$', 'caregiver_client'),
                       )

urlpatterns += patterns('admin_management.client_views', 
                       (r'^client_add/(?P<comp_id>\d+)/$', 'client_add'),
                       (r'^client_add/', 'client_add'),
                       (r'^client_list/', 'client_list'),
                       (r'^client_delete/', 'client_delete'),
                       (r'^client_edit/(?P<client_id>\d+)/$', 'client_edit'),
                       )

urlpatterns += patterns('admin_management.diary_views', 
                       (r'^diary_add/', 'diary_add'),
                       (r'^diary_question/(?P<diary_id>\d+)/(?P<add_ques>\d+)/$', 'diary_question'),
                       (r'^edit_diary_question/(?P<diary_id>\d+)/(?P<ques_id>\d+)/$', 'edit_diary_question'),
                       (r'^delete_diary_question/(?P<diary_id>\d+)/(?P<ques_id>\d+)/$', 'delete_diary_question'),
                       (r'^diary_list/', 'diary_list'),
                       (r'^diary_delete/', 'diary_delete'),
                       (r'^diary_edit/(?P<diary_id>\d+)/$', 'diary_edit'),
                       (r'^diary_question1/(?P<diary_id>\d+)/$', 'diary_question1'),
                       (r'^diary_question_edit/(?P<diary_id>\d+)/(?P<ques_id>\d+)/$', 'diary_question_edit'),
                       (r'^diary_question_delete/(?P<diary_id>\d+)/(?P<ques_id>\d+)/$', 'diary_question_delete'),
                       )
    
urlpatterns += patterns('admin_management.test_views', 
                       (r'^test_add/', 'test_add'),
                       (r'^test_list/', 'test_list'),
                       (r'^test_delete/', 'test_delete'),
                       (r'^test_edit/(?P<test_id>\d+)/$', 'test_edit'),
                       )

urlpatterns += patterns('admin_management.treatment_views', 
                       (r'^treatment/', 'treatment'),
                       (r'^add_module/', 'add_module'),
                       (r'^edit_module/(?P<module_id>\d+)/$', 'edit_module'),
                       (r'^add_session/', 'add_session'),
                       (r'^animation_media/', 'animation_media'),
                       (r'^session/(?P<session_id>\d+)/$', 'session'),
                       (r'^module_list/', 'module_list'),
                       (r'^module_delete/', 'module_delete'),
                       (r'^session_delete/(?P<session_id>\d+)/$', 'session_delete'),
                       (r'^treatment_drag/(?P<module_id>\d+)/(?P<session_id>\d+)/$', 'treatment_drag'),
                       )

urlpatterns += patterns('admin_management.communication_views', 
                       (r'^communication/', 'communication'),
                       (r'^chat_details/(?P<comp_user_id>\d+)/$', 'chat_details'),
                       (r'^chat_persons/(?P<comp_user_id>\d+)/(?P<date>\S+)/$', 'chat_persons'),
                       (r'^chat_history/(?P<comp_user_id>\d+)/(?P<date>\S+)/(?P<user_id>\d+)/$', 'chat_history'),
                       
                       (r'^chat_date/(?P<chat>\d+)/$','chat_date'),
                       (r'^chat/(?P<chat>\d+)/$','chat'),
                       (r'^communication_settings/','communication_settings'),
                       (r'^offline_messages/(?P<msg>\d+)/$','offline_messages'),
                       (r'^message/', 'message'),
                       )

urlpatterns += patterns('admin_management.animation_views', 
                       (r'^animation_add/', 'animation_add'),
                       (r'^animation_list/', 'animation_list'),
                       (r'^animation_delete/', 'animation_delete'),
                       (r'^animation_edit/(?P<animate_id>\d+)/$', 'animation_edit'),
                       )

urlpatterns += patterns('admin_management.plan_views', 
                       (r'^plan_add/', 'plan_add'),
                       (r'^plan_list/', 'plan_list'),
                       (r'^plan_delete/', 'plan_delete'),
                       (r'^plan_edit/(?P<plan_id>\d+)/$', 'plan_edit'),
                       )

urlpatterns += patterns('admin_management.user_views', 
                       (r'^user_list/', 'user_list'),
                       (r'^user_delete/', 'user_delete'),
                       (r'^user_add/', 'user_add'),
                       (r'^user_edit/(?P<user_id>\d+)/$', 'user_edit'),
                       (r'^password_change/', 'password_change'),
                       (r'^password_reset/', 'password_reset'),
                       )


urlpatterns += patterns('admin_management.assignments_views', 
                       (r'^assignments_list/','assignments_list'),
                       (r'^assignments_delete/','assignments_delete'),
                       (r'^assignments/', 'assignments'),
                       (r'^assignments_cluster/(?P<assignment_id>\d+)/$', 'assignments_cluster'),
                       (r'^assignment_question/(?P<cluster_id>\d+)/(?P<quest_id>\d+)/$', 'assignment_question'),
                       (r'^assignment_editquestion/(?P<cluster_id>\d+)/(?P<quest_id>\d+)/$', 'assignment_editquestion'),
                       (r'^assignment_deletequestion/(?P<cluster_id>\d+)/(?P<quest_id>\d+)/$', 'assignment_deletequestion'),
                       (r'^edit_assignments/(?P<assign_id>\d+)/$', 'edit_assignments'),
                       (r'^assignments_editcluster/(?P<assignment_id>\d+)/$', 'assignments_editcluster'),
                       (r'^assignment_clusterdelete/(?P<cluster_id>\d+)/$', 'assignment_clusterdelete'),
                       (r'^assignment_editclustername/(?P<cluster_id>\d+)/$', 'assignment_editclustername'),
                       (r'^delete_assignment/(?P<assign_id>\d+)/$', 'delete_assignment'),
                       )

urlpatterns += patterns('admin_management.questions_views', 
                       (r'^questions_list/', 'questions_list'),
                       (r'^create_questions/(?P<module>\d+)/$', 'create_questions'),
                       (r'^create_questions/', 'create_questions'),
                       (r'^add_module_questions/(?P<module_id>\d+)/$','add_module_questions'),
                       (r'^edit_createquestion/(?P<module_id>\d+)/(?P<question_id>\d+)/$','edit_createquestion'),
                       (r'^question_delete/(?P<module_id>\d+)/(?P<ques_id>\d+)/$','question_delete'),
                       (r'^questions_edit/(?P<module_id>\d+)/$', 'questions_edit'),
                       )

urlpatterns += patterns('admin_management.mail_views', 
                       (r'^mail_configuration/', 'mail_configuration'),
                       (r'^mail_configuration_update/', 'mail_configuration_update'),
                       )