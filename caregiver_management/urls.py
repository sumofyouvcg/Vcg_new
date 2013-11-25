from django.conf.urls.defaults import *

urlpatterns = patterns('caregiver_management.views',
    url(r'^caregiver_home/', 'caregiver_home', name = 'caregiver_home'),
    url(r'^my_profile/', 'my_profile', name = 'caregiver_my_profile'),
)

urlpatterns += patterns('caregiver_management.tasks_views', 
                       url(r'^caregiver_tasks/', 'caregiver_tasks', name = 'caregiver_tasks'),
                       )

urlpatterns += patterns('caregiver_management.message_views', 
                       url(r'^caregiver_message/', 'caregiver_message', name = 'caregiver_message'),
                       
                       url(r'^caregiver_sent_message/', 'caregiver_sent_message', name = 'caregiver_sent_message'),
                       url(r'^caregiver_trash_message/', 'caregiver_trash_message', name = 'caregiver_trash_message'),
                       url(r'^caregiver_message_delete/', 'caregiver_message_delete', name = 'caregiver_message_delete'),
                       url(r'^caregiver_trash_message_delete/', 'caregiver_trash_message_delete', name = 'caregiver_trash_message_delete'),
                       url(r'^caregiver_move_to_inbox/', 'caregiver_move_to_inbox', name = 'caregiver_move_to_inbox'),
                       url(r'^caregiver_sent_message_delete/', 'caregiver_sent_message_delete', name = 'caregiver_sent_message_delete'),
                       
                       url(r'^new_message/', 'new_message', name = 'caregiver_new_message'),
                       url(r'^reply_message/(?P<reply_id>\d+)/$', 'reply_message', name = 'caregiver_reply_message'),
                       url(r'^reply_trash_message/(?P<reply_id>\d+)/$', 'reply_trash_message', name = 'caregiver_reply_trash_message'),
                       url(r'^view_message/(?P<msg_id>\w+)/$', 'view_message', name = 'caregiver_view_message'), 
                       url(r'^view_sent_message/(?P<msg_id>\w+)/$', 'view_sent_message',name = 'caregiver_view_sent_message'),
                       url(r'^view_trash_message/(?P<msg_id>\w+)/$', 'view_trash_message',name = 'caregiver_view_trash_message')
                       )

urlpatterns += patterns('caregiver_management.client_views', 
                       url(r'^client_list/', 'client_list', name = 'caregiver_client_list'),
                       url(r'^client_add/$','client_add', name = 'caregiver_client_add'),
                       url(r'^client_home/(?P<client_id>\d+)/$','client_home', name = 'caregiver_client_home'),
                       url(r'^client_details/(?P<client_id>\d+)/$','client_details', name = 'caregiver_client_details'),
                       url(r'^client_managing_details/(?P<client_id>\d+)/$','client_managing_details', name = 'caregiver_client_managing_details'),
                                              
                       url(r'^client_caregivers/(?P<client_id>\d+)/$', 'client_caregivers', name = 'caregiver_client_caregivers'),
                       url(r'^client_caregiver_details/(?P<client_id>\d+)/(?P<caregiver_id>\d+)/$', 'client_caregiver_details', name = 'caregiver_client_caregiver_details'),
 
                       url(r'^client_moniter_list/(?P<client_id>\d+)/$', 'client_moniter_list', name = 'caregiver_client_moniter_list'),
                       url(r'^client_caregiver_chat/(?P<client_id>\d+)/$', 'client_caregiver_chat', name = 'caregiver_client_caregiver_chat'),
                       url(r'^client_caregiver_video/(?P<client_id>\d+)/$', 'client_caregiver_video', name = 'caregiver_client_caregiver_video'),
                       url(r'^video_details/(?P<client_id>\d+)/$', 'video_details', name = 'caregiver_video_details'),
                       )
urlpatterns += patterns('caregiver_management.caregiver_treatment_views', 
                       url(r'^client_treatment_list/(?P<client_id>\d+)/$', 'client_treatment_list', name ='caregiver_client_treatment_list'),
                       url(r'^client_treatment_add/(?P<client_id>\d+)/$', 'client_treatment_add', name ='caregiver_client_treatment_add'),
                       url(r'^client_treatment_edit/(?P<client_id>\d+)/(?P<company_id>\d+)/$', 'client_treatment_edit', name ='caregiver_client_treatment_edit'),
                       url(r'^client_treatment_custom/(?P<client_id>\d+)/(?P<module_id>\d+)/$', 'client_treatment_custom', name ='caregiver_client_treatment_custom'),
                       url(r'^client_treatment_view/(?P<client_id>\d+)/(?P<module_id>\d+)/$', 'client_treatment_view', name ='caregiver_client_treatment_view'),
                       url(r'^client_treatment_session/(?P<client_id>\d+)/(?P<session_id>\d+)/$', 'client_treatment_session', name ='caregiver_client_treatment_session'),
                       url(r'^client_session_delete/(?P<client_id>\d+)/(?P<session_id>\d+)/$', 'client_session_delete', name ='caregiver_client_session_delete'),
                       url(r'^client_treatment_custom/session_choice/(?P<module_id>\w+)/(?P<client_id>\d+)/(?P<treat_mod_id>\d+)/$', 'client_session_choices', name ='caregiver_client_session_choices'),
                       url(r'^client_treatment_delete/(?P<client_id>\d+)/$', 'client_treatment_delete', name ='caregiver_client_treatment_delete'),
                       )

urlpatterns += patterns('caregiver_management.client_plan_views', 
                       url(r'^client_plan_list/(?P<client_id>\d+)/$', 'client_plan_list', name ='caregiver_client_plan_list'),
                       url(r'^client_plan_delete/(?P<client_id>\d+)/$', 'client_plan_delete', name ='caregiver_client_plan_delete'),
                       url(r'^client_plan_add/(?P<client_id>\d+)/$', 'client_plan_add', name ='caregiver_client_plan_add'),
                       url(r'^client_plan_edit/(?P<client_id>\d+)/(?P<plan_id>\d+)/$', 'client_plan_edit', name ='caregiver_client_plan_edit'),
                       url(r'^client_plan_view/(?P<client_id>\d+)/(?P<plan_id>\d+)/$', 'client_plan_view', name ='caregiver_client_plan_view'),
                       )

urlpatterns += patterns('caregiver_management.client_test_views', 
                       url(r'^client_test_list/(?P<client_id>\d+)/$', 'client_test_list', name ='caregiver_client_test_list'),
                       url(r'^client_test_add/(?P<client_id>\d+)/$', 'client_test_add', name ='caregiver_client_test_add'),
                       url(r'^client_test_view/(?P<client_id>\d+)/(?P<test_id>\d+)/$', 'client_test_view', name ='caregiver_client_test_view'),
                       url(r'^client_test_edit/(?P<client_id>\d+)/(?P<test_id>\d+)/$', 'client_test_edit', name ='caregiver_client_test_edit'),
                       url(r'^client_test_delete/(?P<client_id>\d+)/$', 'client_test_delete', name ='caregiver_client_test_delete'),
                       url(r'^client_test_feedback/(?P<client_id>\d+)/(?P<test_id>\d+)/$', 'client_test_feedback', name ='caregiver_client_test_feedback'),
                       )

urlpatterns += patterns('caregiver_management.client_diary_views', 
                       url(r'^client_diary_list/(?P<client_id>\d+)/$', 'client_diary_list', name ='caregiver_client_diary_list'),
                       url(r'^client_diary_add/(?P<client_id>\d+)/$', 'client_diary_add', name ='caregiver_client_diary_add'),
                       url(r'^client_diary_delete/(?P<client_id>\d+)/$', 'client_diary_delete', name ='caregiver_client_diary_delete'),
                       url(r'^client_diary_show/(?P<client_id>\d+)/(?P<diary_id>\d+)/$', 'client_diary_show', name ='caregiver_client_diary_show'),
                       url(r'^client_diary_view/(?P<client_id>\d+)/(?P<diary_id>\d+)/(?P<date>\S+)/$', 'client_diary_view', name ='caregiver_client_diary_view'),
                       url(r'^client_diary_today/(?P<client_id>\d+)/(?P<diary_id>\d+)/(?P<current_date>\S+)/$', 'client_diary_today', name ='caregiver_client_diary_today'),
                       url(r'^client_diary_edit/(?P<client_id>\d+)/(?P<diary_id>\d+)/$', 'client_diary_edit', name ='caregiver_client_diary_edit'),
                       )

urlpatterns += patterns('caregiver_management.user_views', 
                       url(r'^password_change/', 'password_change', name = 'caregiver_password_change'),
                       )
urlpatterns += patterns('caregiver_management.client_assignment_views', 
                       url(r'^client_assignment_list/(?P<client_id>\d+)/$', 'client_assignment_list', name ='caregiver_client_assignment_list'),
                       url(r'^client_assignment_details/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_details', name ='caregiver_client_assignment_details'),
                       url(r'^client_assignment_add/(?P<client_id>\d+)/$', 'client_assignment_add', name ='caregiver_client_assignment_add'),
                       url(r'^client_assignment_view/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_view', name ='caregiver_client_assignment_view'),
                       url(r'^client_assignment_edit/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_edit', name ='caregiver_client_assignment_edit'),
                       url(r'^client_assignment_questions/(?P<client_id>\d+)/(?P<assign_id>\d+)/(?P<cluster_id>\d+)/$', 'client_assignment_questions', name ='caregiver_client_assignment_questions'),
                       url(r'^client_assignment_delete/(?P<client_id>\d+)/$', 'client_assignment_delete', name ='caregiver_client_assignment_delete'),
                       )

urlpatterns += patterns('caregiver_management.client_message_views', 
                       url(r'^client_send_message/(?P<client_id>\d+)/$', 'client_send_message', name = 'caregiver_client_send_message'),
                       url(r'^client_reply_message/(?P<client_id>\d+)/(?P<msg_id>\d+)/$', 'client_reply_message', name = 'caregiver_client_reply_message'),
                       url(r'^client_view_message/(?P<client_id>\d+)/(?P<msg_id>\d+)/$', 'client_view_message', name = 'caregiver_client_view_message'),
                       url(r'^client_messages/(?P<client_id>\d+)/$', 'client_messages', name = 'caregiver_client_messages'),
                       url(r'^client_messages_delete/(?P<client_id>\d+)/$', 'client_messages_delete', name = 'caregiver_client_messages_delete'),

                       )

urlpatterns += patterns('caregiver_management.client_animation_views', 
                       url(r'^client_animation_list/(?P<client_id>\d+)/$', 'client_animation_list', name = 'caregiver_client_animation_list'),
                       url(r'^client_animation_delete/(?P<client_id>\d+)/$', 'client_animation_delete', name = 'caregiver_client_animation_delete'),
                       url(r'^client_animation_add/(?P<client_id>\d+)/$', 'client_animation_add', name = 'caregiver_client_animation_add'),
                       url(r'^client_animation_edit/(?P<client_id>\d+)/(?P<animation_id>\d+)/$', 'client_animation_edit', name = 'caregiver_client_animation_edit'),
                       url(r'^client_animation_view/(?P<client_id>\d+)/(?P<animation_id>\d+)/$', 'client_animation_view', name = 'caregiver_client_animation_view'),
                       )

urlpatterns += patterns('caregiver_management.caregiver_chat_views', 
                       url(r'^caregiver_chat_details/$', 'caregiver_chat_details', name="caregiver_chat_details"),
                       url(r'^caregiver_chat_persons/(?P<date>\S+)/$', 'caregiver_chat_persons', name="caregiver_chat_persons"),
                       url(r'^caregiver_chat_history/(?P<date>\S+)/(?P<user_id>\d+)/$', 'caregiver_chat_history', name="caregiver_chat_history"),
                       url(r'^chat_old_details/(?P<username>\w+)/$', 'chat_old_details', name="caregiver_chat_old_details"),
                       url(r'^chat_user/$', 'chat_user', name="caregiver_chat_user"),
                       url(r'^post/$', 'post', name="caregiver_post"),
                       url(r'^get/$', 'get', name="caregiver_get"),
                       )

urlpatterns += patterns('caregiver_management.client_chat_views', 
                       url(r'^chat_details/(?P<client_id>\d+)/$', 'chat_details', name="caregiver_client_chat_details"),
                       url(r'^chat_history/(?P<client_id>\d+)/(?P<date>\S+)/$', 'chat_history', name="caregiver_client_chat_history"),
                       )

urlpatterns += patterns('caregiver_management.caregiver_form_views', 
                       url(r'^client_forms_list/(?P<client_id>\d+)/$', 'client_forms_list', name = 'caregiver_client_forms_list'),
                       url(r'^client_forms_add/(?P<client_id>\d+)/$', 'client_forms_add', name = 'caregiver_client_forms_add'),
                       url(r'^client_forms_edit/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_forms_edit', name = 'caregiver_client_forms_edit'),
                       url(r'^client_forms_view/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_forms_view', name = 'caregiver_client_forms_view'),
                       url(r'^client_forms_delete/(?P<client_id>\d+)/$', 'client_forms_delete', name = 'caregiver_client_forms_delete'),
                       )

urlpatterns += patterns('caregiver_management.client_intake_form_views',
                       url(r'^client_intake_form/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_intake_form', name = 'caregiver_client_intake_form'),
                       url(r'^client_intake_form_completed/(?P<client_id>\d+)/(?P<form_id>\d+)/(?P<intake_id>\d+)/$', 'client_intake_form_completed', name = 'caregiver_client_intake_form_completed'),
                       )

urlpatterns += patterns('caregiver_management.client_treatment_agreement_form_views',
                       url(r'^client_treatment_agreement_form/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_treatment_agreement_form', name = 'caregiver_client_treatment_agreement_form'),
                       url(r'^client_treatment_agreement_form_completed/(?P<client_id>\d+)/(?P<form_id>\d+)/(?P<treat_agree_id>\d+)/$', 'client_treatment_agreement_form_completed', name = 'caregiver_client_treatment_agreement_form_completed'),
                       )

urlpatterns += patterns('caregiver_management.client_treatment_form_views',
                       url(r'^client_treatment_form/(?P<client_id>\d+)/(?P<form_id>\d+)/$', 'client_treatment_form', name = 'caregiver_client_treatment_form'),
                       url(r'^client_treatment_form_completed/(?P<client_id>\d+)/(?P<form_id>\d+)/(?P<treat_id>\d+)/$', 'client_treatment_form_completed', name = 'caregiver_client_treatment_form_completed'),
                       )