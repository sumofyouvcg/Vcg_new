from django.conf.urls.defaults import *

urlpatterns = patterns('company_management.views',
                        url(r'^company_home/', 'company_home', name = 'company_home'),
                        url(r'^my_profile/', 'my_profile', name = 'company_my_profile'),
)

urlpatterns += patterns('company_management.tasks_views', 
                       url(r'^company_tasks/', 'company_tasks', name = 'company_tasks'),
                       )

urlpatterns += patterns('company_management.message_views', 
                       url(r'^company_message/', 'company_message', name = 'company_message' ),
                       url(r'^company_sent_message/', 'company_sent_message', name = 'company_sent_message'),
                       url(r'^company_trash_message/', 'company_trash_message', name = 'company_trash_message'),
                       url(r'^company_message_delete/', 'company_message_delete', name = 'company_message_delete'),
                       url(r'^company_trash_message_delete/', 'company_trash_message_delete', name = 'company_trash_message_delete'),
                       url(r'^company_move_to_inbox/', 'company_move_to_inbox', name = 'company_move_to_inbox'),
                       url(r'^company_sent_message_delete/', 'company_sent_message_delete', name = 'company_sent_message_delete'),
                       
                       url(r'^new_message/', 'new_message', name ='company_new_message'),
                       url(r'^reply_message/(?P<reply_id>\d+)/$', 'reply_message', name ='company_reply_message'),
                       url(r'^reply_trash_message/(?P<reply_id>\d+)/$', 'reply_trash_message', name = 'company_reply_trash_message'),
                       url(r'^view_message/(?P<msg_id>\w+)/$', 'view_message', name = 'company_view_message'),
                       url(r'^view_sent_message/(?P<msg_id>\w+)/$', 'view_sent_message', name = 'company_view_sent_message'),                            
                       url(r'^view_trash_message/(?P<msg_id>\w+)/$', 'view_trash_message', name = 'company_view_trash_message'),
                       )

urlpatterns += patterns('company_management.client_views', 
                       url(r'^client_list/', 'client_list', name = 'company_client_list'),
                       url(r'^client_add/(?P<company_id>\d+)/$','client_add', name = 'company_client_add'),
                       url(r'^client_home/(?P<client_id>\d+)/$','client_home', name = 'company_client_home'),
                       url(r'^client_details/(?P<client_id>\d+)/$','client_details', name = 'company_client_details'),
                       
                       url(r'^client_moniter_list/(?P<client_id>\d+)/$', 'client_moniter_list', name = 'company_client_moniter_list'),
                       url(r'^client_caregiver_chat/(?P<client_id>\d+)/$', 'client_caregiver_chat', name = 'company_client_caregiver_chat'),
                       url(r'^client_caregiver_video/(?P<client_id>\d+)/$', 'client_caregiver_video', name = 'company_client_caregiver_video'),
		               url(r'^video_details/(?P<client_id>\d+)/$', 'video_details', name = 'company_video_details'),

                       )
urlpatterns += patterns('company_management.client_message_views', 
                       url(r'^client_send_message/(?P<client_id>\d+)/$', 'client_send_message', name = 'company_client_send_message'),
                       url(r'^client_reply_message/(?P<client_id>\d+)/(?P<msg_id>\d+)/$', 'client_reply_message', name = 'company_client_reply_message'),
                       url(r'^client_messages/(?P<client_id>\d+)/$', 'client_messages', name = 'company_client_messages'),
                       url(r'^client_messages_delete/(?P<client_id>\d+)/$', 'client_messages_delete', name = 'company_client_messages_delete'),
                       url(r'^client_view_message/(?P<client_id>\d+)/(?P<msg_id>\d+)/$', 'client_view_message', name = 'company_client_view_message'),

                       )

urlpatterns += patterns('company_management.client_caregivers_views', 
                       url(r'^client_caregivers/(?P<client_id>\d+)/$', 'client_caregivers', name = 'company_client_caregivers'),
                       url(r'^client_caregiver_details/(?P<client_id>\d+)/(?P<caregiver_id>\d+)/$', 'client_caregiver_details', name = 'company_client_caregiver_details'),
                       )

urlpatterns += patterns('company_management.client_diary_views', 
                       url(r'^client_diary_list/(?P<client_id>\d+)/$', 'client_diary_list', name = 'company_client_diary_list'),
                       url(r'^client_diary_delete/(?P<client_id>\d+)/$', 'client_diary_delete', name = 'company_client_diary_delete'),
                       url(r'^client_diary_add/(?P<client_id>\d+)/$', 'client_diary_add', name = 'company_client_diary_add'),
                       url(r'^client_diary_show/(?P<client_id>\d+)/(?P<diary_id>\d+)/$', 'client_diary_show', name = 'company_client_diary_show'),
                       url(r'^client_diary_view/(?P<client_id>\d+)/(?P<diary_id>\d+)/(?P<date>\S+)/$', 'client_diary_view', name = 'company_client_diary_view'),
                       url(r'^client_diary_today/(?P<client_id>\d+)/(?P<diary_id>\d+)/(?P<current_date>\S+)/$', 'client_diary_today', name = 'company_client_diary_today'),
                       url(r'^client_diary_edit/(?P<client_id>\d+)/(?P<diary_id>\d+)/$', 'client_diary_edit', name = 'company_client_diary_edit'),
                       )

urlpatterns += patterns('company_management.client_test_views', 
                       url(r'^client_test_list/(?P<client_id>\d+)/$', 'client_test_list', name = 'company_client_test_list'),
                       url(r'^client_test_delete/(?P<client_id>\d+)/$', 'client_test_delete', name = 'company_client_test_delete'),
                       url(r'^client_test_add/(?P<client_id>\d+)/$', 'client_test_add', name = 'company_client_test_add'),
                       url(r'^client_test_view/(?P<client_id>\d+)/(?P<test_id>\d+)/$', 'client_test_view', name = 'company_client_test_view'),
                       url(r'^client_test_edit/(?P<client_id>\d+)/(?P<test_id>\d+)/$', 'client_test_edit', name = 'company_client_test_edit'),
                       url(r'^client_test_feedback/(?P<client_id>\d+)/(?P<test_id>\d+)/$', 'client_test_feedback', name = 'company_client_test_feedback'),
                       )

urlpatterns += patterns('company_management.client_plan_views', 
                       url(r'^client_plan_list/(?P<client_id>\d+)/$', 'client_plan_list', name = 'company_client_plan_list'),
                       url(r'^client_plan_delete/(?P<client_id>\d+)/$', 'client_plan_delete', name = 'company_client_plan_delete'),
                       url(r'^client_plan_add/(?P<client_id>\d+)/$', 'client_plan_add', name = 'company_client_plan_add'),
                       url(r'^client_plan_edit/(?P<client_id>\d+)/(?P<plan_id>\d+)/$', 'client_plan_edit', name = 'company_client_plan_edit'),
                       url(r'^client_plan_view/(?P<client_id>\d+)/(?P<plan_id>\d+)/$', 'client_plan_view', name = 'company_client_plan_view'),
                       
                       )

urlpatterns += patterns('company_management.caregivers_views', 
                       url(r'^caregivers_list/', 'caregivers_list', name = 'company_caregivers_list'),
                       url(r'^caregivers_delete/', 'caregivers_delete', name = 'company_caregivers_delete'),
                       url(r'^caregivers_add/(?P<company_id>\d+)/$','caregivers_add', name = 'company_caregivers_add'),
                       url(r'^caregivers_edit/(?P<company_id>\d+)/(?P<caregiver_id>\d+)/$','caregivers_edit', name = 'company_caregivers_edit'),
                       url(r'^caregiver_view/', 'caregiver_view', name = 'company_caregiver_view'),
		               url(r'^company_caregiver_client/', 'company_caregiver_client', name = 'company_caregiver_client'),
                       )

urlpatterns += patterns('company_management.configuration_views', 
                       url(r'^configuration_contact/', 'configuration_contact', name = 'company_configuration_contact'),
                       url(r'^config_contact_update/(?P<company_id>\d+)/$', 'config_contact_update', name = 'company_config_contact_update'),
                       url(r'^configuration_domain/', 'configuration_domain', name = 'company_configuration_domain'),
                       url(r'^configuration_layout/', 'configuration_layout', name = 'company_configuration_layout'),
                       url(r'^config_layout_update/(?P<company_id>\d+)/$', 'config_layout_update', name = 'company_config_layout_update'),
                       url(r'^configuration_home_page/', 'configuration_home_page', name = 'company_configuration_home_page'),
                       url(r'^config_homepage_update/(?P<company_id>\d+)/$', 'config_homepage_update', name = 'company_config_homepage_update'),
                       url(r'^configuration_location/', 'configuration_location', name = 'company_configuration_location'),
                       url(r'^config_location_update/(?P<company_id>\d+)/$', 'config_location_update', name = 'company_config_location_update'),
                       )

urlpatterns += patterns('company_management.client_treatment_views', 
                       url(r'^client_treatment_list/(?P<client_id>\d+)/$', 'client_treatment_list', name = 'company_client_treatment_list'),
                       url(r'^client_treatment_add/(?P<client_id>\d+)/$', 'client_treatment_add', name = 'company_client_treatment_add'),
                       url(r'^client_treatment_edit/(?P<client_id>\d+)/(?P<company_id>\d+)/$', 'client_treatment_edit', name = 'company_client_treatment_edit'),
                       url(r'^client_treatment_custom/(?P<client_id>\d+)/(?P<module_id>\d+)/$', 'client_treatment_custom', name = 'company_client_treatment_custom'),
                       url(r'^client_treatment_view/(?P<client_id>\d+)/(?P<module_id>\d+)/$', 'client_treatment_view', name = 'company_client_treatment_view'),
                       url(r'^client_treatment_session/(?P<client_id>\d+)/(?P<session_id>\d+)/$', 'client_treatment_session', name = 'company_client_treatment_session'),
                       url(r'^client_session_delete/(?P<client_id>\d+)/(?P<session_id>\d+)/$', 'client_session_delete', name = 'company_client_session_delete'),
                       url(r'^client_treatment_custom/session_choice/(?P<module_id>\w+)/(?P<client_id>\d+)/(?P<treat_mod_id>\d+)/$', 'client_session_choices', name = 'company_client_session_choices'),
                       url(r'^client_treatment_delete/(?P<client_id>\d+)/$', 'client_treatment_delete', name = 'company_client_treatment_delete'),
                       )

urlpatterns += patterns('company_management.user_views', 
                       url(r'^password_change/', 'password_change', name = 'company_password_change'),
                       url(r'^password_reset/', 'password_reset', name = 'company_password_reset'),
                       )

urlpatterns += patterns('company_management.client_assignment_views', 
                       url(r'^client_assignment_list/(?P<client_id>\d+)/$', 'client_assignment_list', name = 'company_client_assignment_list'),
                       url(r'^client_assignment_delete/(?P<client_id>\d+)/$', 'client_assignment_delete', name = 'company_client_assignment_delete'),
                       url(r'^client_assignment_details/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_details', name = 'company_client_assignment_details'),
                       url(r'^client_assignment_add/(?P<client_id>\d+)/$', 'client_assignment_add', name = 'company_client_assignment_add'),
                       url(r'^client_assignment_view/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_view', name = 'company_client_assignment_view'),
                       url(r'^client_assignment_edit/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_edit', name = 'company_client_assignment_edit'),
                       url(r'^client_assignment_questions/(?P<client_id>\d+)/(?P<assign_id>\d+)/(?P<cluster_id>\d+)/$', 'client_assignment_questions', name = 'company_client_assignment_questions'),
                       url(r'^client_assignment_delete/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_delete', name = 'company_client_assignment_questions'),
                       )

urlpatterns += patterns('company_management.client_animation_views', 
                       url(r'^client_animation_list/(?P<client_id>\d+)/$', 'client_animation_list', name = 'company_client_animation_list'),
                       url(r'^client_animation_add/(?P<client_id>\d+)/$', 'client_animation_add', name = 'company_client_animation_add'),
                       url(r'^client_animation_edit/(?P<client_id>\d+)/(?P<animation_id>\d+)/$', 'client_animation_edit', name = 'company_client_animation_edit'),
                       url(r'^client_animation_view/(?P<client_id>\d+)/(?P<animation_id>\d+)/$', 'client_animation_view', name = 'company_client_animation_view'),
                       url(r'^client_animation_delete/(?P<client_id>\d+)/$', 'client_animation_delete', name = 'company_client_animation_delete'),
                       )

urlpatterns += patterns('company_management.company_chat_views', 
                       url(r'^company_chat_details/$', 'company_chat_details', name = 'company_chat_details'),
                       url(r'^company_chat_persons/(?P<date>\S+)/$', 'company_chat_persons', name = 'company_chat_persons'),
                       url(r'^company_chat_history/(?P<date>\S+)/(?P<user_id>\d+)/$', 'company_chat_history', name = 'company_chat_history'),
                       url(r'^chat_old_details/(?P<username>\w+)/$', 'chat_old_details', name = 'company_chat_old_details'),
                       url(r'^chat_user/$', 'chat_user', name = 'company_chat_user'),
                       url(r'^post/$', 'post', name = 'company_post'),
                       url(r'^get/$', 'get', name = 'company_get'),
                       )

urlpatterns += patterns('company_management.client_chat_views', 
                       url(r'^chat_details/(?P<client_id>\d+)/$', 'chat_details', name = 'company_client_chat_details'),
                       url(r'^chat_history/(?P<client_id>\d+)/(?P<date>\S+)/$', 'chat_history', name = 'company_client_chat_history'),
                       )

urlpatterns += patterns('company_management.company_form_views', 
                       url(r'^client_forms_list/(?P<client_id>\d+)/$', 'client_forms_list', name = 'company_client_forms_list'),
                       url(r'^client_forms_add/(?P<client_id>\d+)/$', 'client_forms_add', name = 'company_client_forms_add'),
                       url(r'^client_forms_edit/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_forms_edit', name = 'company_client_forms_edit'),
                       url(r'^client_forms_view/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_forms_view', name = 'company_client_forms_view'),
                       url(r'^client_forms_delete/(?P<client_id>\d+)/$', 'client_forms_delete', name = 'company_client_forms_delete'),
                       )

urlpatterns += patterns('company_management.client_intake_form_views',
                       url(r'^client_intake_form/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_intake_form', name = 'company_client_intake_form'),
                       url(r'^client_intake_form_completed/(?P<client_id>\d+)/(?P<form_id>\d+)/(?P<intake_id>\d+)/$', 'client_intake_form_completed', name = 'company_client_intake_form_completed'),
                       )

urlpatterns += patterns('company_management.client_treatment_agreement_form_views',
                       url(r'^client_treatment_agreement_form/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_treatment_agreement_form', name = 'company_client_treatment_agreement_form'),
                       url(r'^client_treatment_agreement_form_completed/(?P<client_id>\d+)/(?P<form_id>\d+)/(?P<treat_agree_id>\d+)/$', 'client_treatment_agreement_form_completed', name = 'company_client_treatment_agreement_form_completed'),
                       )

urlpatterns += patterns('company_management.client_treatment_form_views',
                       url(r'^client_treatment_form/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_treatment_form', name = 'company_client_treatment_form'),
                       url(r'^client_treatment_form_completed/(?P<client_id>\d+)/(?P<form_id>\d+)/(?P<treat_id>\d+)/$', 'client_treatment_form_completed', name = 'company_client_treatment_form_completed'),
                       )
