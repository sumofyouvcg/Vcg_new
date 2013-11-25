from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

from vcg.admin_management.views import home, login_user, user_list, user_edit

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vcg.views.home', name='home'),
    # url(r'^vcg/', include('vcg.foo.urls')),

    (r'^$', login_user),
    (r'^(?P<domain_name>\w+)/$', login_user),
    (r'^administrator/', home),
    url(r'^vcg/admin/', include(admin.site.urls)),
    (r'^admin_management/',include('admin_management.urls')),
    (r'^(?P<domain_name>\w+)/company_management/',include('company_management.urls')),
    (r'^(?P<domain_name>\w+)/client_management/',include('client_management.urls')),
    (r'^(?P<domain_name>\w+)/caregiver_management/',include('caregiver_management.urls')),
    (r'^admin_user/logout/$', 'admin_management.views.logout_user'),
    (r'^(?P<domain_name>\w+)/logout/$', 'admin_management.views.logout_user'),
    (r'^user_list/', user_list),
    (r'^user_edit/', user_edit),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^set_lang', 'vcg.admin_management.views.set_lang', name='set_lang'),
    (r'^vchat_req', 'vcg.admin_management.views.vchat_req'),
    (r'^vchat_join', 'vcg.admin_management.views.vchat_join'),
)

urlpatterns += patterns('',
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.generic.simple.redirect_to', {'url': '/static/%(path)s/'}),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
