from django.conf.urls.defaults import *

urlpatterns = patterns('client_management.views', 
                       url(r'^client_home/','client_home', name = 'client_home'),
                       url(r'^my_profile/','my_profile', name = 'client_my_profile'),
                       )

urlpatterns += patterns('client_management.client_task_views', 
                       url(r'^task_list/','task_list', name = 'client_task_list'),
                       )
urlpatterns += patterns('client_management.client_msg_views', 
                       url(r'^client_message/','client_message', name = 'client_message'),
                       url(r'^client_reply_message/(?P<reply_id>\d+)/$','client_reply_message', name = 'client_reply_message'),
                       url(r'^client_reply_trash_message/(?P<reply_id>\d+)/$','client_reply_trash_message', name = 'client_reply_trash_message'),

                       url(r'^message_list/','message_list', name = 'client_message_list'),
                       url(r'^sent_message_list/','sent_message_list', name = 'client_sent_message_list'),
                       url(r'^trash_message_list/','trash_message_list', name = 'client_trash_message_list'),
                       
                       url(r'^client_view_message/(?P<msg_id>\w+)/$','client_view_message', name = 'client_view_message'),
                       url(r'^client_view_sent_message/(?P<msg_id>\w+)/$','client_view_sent_message', name = 'client_view_sent_message'),
                       url(r'^client_view_trash_message/(?P<msg_id>\w+)/$','client_view_trash_message', name = 'client_view_trash_message'),
                       
                       url(r'^message_delete/', 'message_delete', name = 'client_message_delete'),
                       url(r'^sent_message_delete/', 'sent_message_delete', name = 'client_sent_message_delete'),
                       url(r'^trash_message_delete/', 'trash_message_delete', name = 'client_trash_message_delete'),
                       url(r'^client_move_to_inbox/', 'client_move_to_inbox', name = 'client_move_to_inbox'),
                       )

urlpatterns += patterns('client_management.client_plan_views', 
                       url(r'^plan_list/','plan_list', name = 'client_plan_list'),
                       url(r'^client_plan_view/(?P<plan_id>\d+)/(?P<another_action>\d+)/$', 'client_plan_view', name = 'client_plan_view'),
                       url(r'^client_plan_edit/(?P<plan_id>\d+)/(?P<action_id>\d+)/$', 'client_plan_edit', name = 'client_plan_edit'),
                       url(r'^client_plan_delete/(?P<plan_id>\d+)/(?P<action_id>\d+)/$', 'client_plan_delete', name = 'client_plan_delete'),
                       url(r'^client_plan_feedback/(?P<plan_id>\d+)/$','client_plan_feedback', name = 'client_plan_feedback'),
                       )

urlpatterns += patterns('client_management.client_test_views', 
                       url(r'^test_list/','test_list', name = 'client_test_list'),
                       url(r'^test_details/(?P<test_id>\d+)/$','test_details', name = 'client_test_details'),
                       url(r'^client_test_completed/(?P<test_id>\d+)/$','client_test_completed', name = 'client_test_completed'),
                       url(r'^client_test_feedback/(?P<test_id>\d+)/$','client_test_feedback', name = 'client_test_feedback'),
                       )

urlpatterns += patterns('client_management.client_diary_views', 
                       url(r'^diary_list/','diary_list', name = 'client_diary_list'),
                       url(r'^diary_show/(?P<diary_id>\d+)/$','diary_show', name = 'client_diary_show'),
                       url(r'^diary_view/(?P<diary_id>\d+)/(?P<current_date>\S+)/$','diary_view', name = 'client_diary_view'),
                       url(r'^diary_view_details/(?P<diary_id>\d+)/(?P<date>\S+)/$','diary_view_details', name = 'client_diary_view_details'),
                       url(r'^webcam/','webcam', name = 'client_webcam'),
                       url(r'^chat/','chat', name = 'client_chat'),
                       url(r'^add_chat/','add_chat', name = 'client_add_chat'),
                       )

urlpatterns += patterns('client_management.client_questions_views', 
                       url(r'^questions_list/','questions_list', name = 'client_questions_list'),
                       url(r'^client_question_view/(?P<treat_id>\d+)/$','client_question_view', name = 'client_question_view'),
                       url(r'^client_question_feedback/(?P<module_id>\d+)/$','client_question_feedback', name = 'client_question_feedback'),
                       )

urlpatterns += patterns('client_management.clienttreatment_views', 
                       url(r'^treatment_list/','treatment_list', name = 'client_treatment_list'),
                       url(r'^treatment_view/(?P<module_id>\d+)/$','treatment_view', name = 'client_treatment_view'),
                       url(r'^treatment_session/(?P<session_id>\d+)/$','treatment_session', name = 'client_treatment_session'),
                       )

urlpatterns += patterns('client_management.client_assignment_views', 
                       url(r'^client_assignment_list/', 'client_assignment_list', name = 'client_assignment_list'),
                       url(r'^client_assignment_questions/(?P<assign_id>\d+)/$', 'client_assignment_questions', name = 'client_assignment_questions'),
                       url(r'^client_assignment_completed/(?P<assign_id>\d+)/$', 'client_assignment_completed', name = 'client_assignment_completed'),
                       url(r'^client_assignment_feedback/(?P<assign_id>\d+)/$','client_assignment_feedback', name = 'client_assignment_feedback'),
#                       (r'^client_assignment_add/(?P<client_id>\d+)/$', 'client_assignment_add'),
#                       (r'^client_assignment_view/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_view'),
#                       (r'^client_assignment_edit/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_edit'),
                       url(r'^client_assignment_questions/(?P<client_id>\d+)/(?P<assign_id>\d+)/(?P<cluster_id>\d+)/$', 'client_assignment_questions', name = 'client_assignment_questions'),
#                       (r'^client_assignment_delete/(?P<client_id>\d+)/(?P<assign_id>\d+)/$', 'client_assignment_delete'),
                       )

urlpatterns += patterns('client_management.user_views', 
                       url(r'^password_change/', 'password_change', name = 'client_password_change'),
                       )

urlpatterns += patterns('client_management.client_animation_views', 
                       url(r'^animation_list/','animation_list', name = 'client_animation_list'),
                       url(r'^client_animation_view/(?P<animation_id>\d+)/$', 'client_animation_view', name = 'client_animation_view'),
                       )

urlpatterns += patterns('client_management.client_chat_views', 
                       url(r'^chat_details/$', 'chat_details', name = 'client_chat_details'),
                       url(r'^chat_persons/(?P<date>\S+)/$', 'chat_persons', name = 'client_chat_persons'),
                       url(r'^chat_history/(?P<date>\S+)/(?P<user_id>\d+)/$', 'chat_history', name = 'client_chat_history'),
                       url(r'^chat_old_details/(?P<username>\w+)/$', 'chat_old_details', name = 'client_chat_old_details'),
                       url(r'^chat_user/$', 'chat_user', name = 'client_chat_user'),
                       url(r'^post/$', 'post', name = 'client_post'),
                       url(r'^get/$', 'get', name = 'client_get'),
                       )

urlpatterns += patterns('client_management.client_forms_views', 
                       url(r'^forms_list/','forms_list', name = 'client_forms_list'),
                       url(r'^client_forms_view/(?P<form_id>\d+)/$', 'client_forms_view', name = 'client_forms_view'),
                       )

urlpatterns += patterns('client_management.client_intake_form_views', 
                       url(r'^client_intake_form/(?P<form_id>\d+)/$', 'client_intake_form', name = 'client_intake_form'),
                       url(r'^client_intake_form_feedback/(?P<intake_id>\d+)/$', 'client_intake_form_feedback', name = 'client_intake_form_feedback'),
                       )

urlpatterns += patterns('client_management.client_treatment_agreement_form_views', 
                       url(r'^client_treatment_agreement_form/(?P<form_id>\d+)/$', 'client_treatment_agreement_form', name = 'client_treatment_agreement_form'),
                       url(r'^client_treatment_agreement_form_feedback/(?P<treat_agree_id>\d+)/$', 'client_treatment_agreement_form_feedback', name = 'client_treatment_agreement_form_feedback'),
                       )

urlpatterns += patterns('client_management.client_treatment_form_views',
                       url(r'^client_treatment_form/(?P<form_id>\d+)/$', 'client_treatment_form', name = 'client_client_treatment_form'),
                       url(r'^client_treatment_form_completed/(?P<treat_id>\d+)/$', 'client_treatment_form_completed', name = 'client_client_treatment_form_completed'),
                       )