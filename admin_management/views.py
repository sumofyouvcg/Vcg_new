import OpenTokSDK

from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils import simplejson

from vcg.admin_management.models import AdminUserPermission, Company, Caregiver,  Client, AdminUser, VideoSession
from vcg.company_management.models import ConfigurationLogo
from vcg.client_management.models import ChatMessage

@login_required
def home(request):
    if not request.user.is_superuser:
        auth_views = AdminUserPermission.objects.filter(admin_user__user_id = request.user)
        if auth_views:
            return render_to_response('base.html', locals(), context_instance=RequestContext(request))
    return redirect('/admin_management/company_list/')

def login_user(request, domain_name = None):
    state = ""
    company_logo = ConfigurationLogo.objects.filter(company__sub_domain = domain_name)
    if company_logo:
        company_logo_icon = company_logo[0]
                                    
    if domain_name == "logout":
        return HttpResponseRedirect('/admin_user/logout/')
    elif domain_name:
        get_object_or_404(Company, sub_domain = domain_name)

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                company = Company.objects.filter(company_number = username, active = True)
                caregiver = Caregiver.objects.filter(caregiver_number = username, active = True, company__active = True)
                client = Client.objects.filter(client_number = username, active = True, company__active = True)
                admin = AdminUser.objects.filter(user_id = username, active = True)
                if not company and not caregiver and not client and not admin and not request.user.is_superuser:
                    messages.success(request, _("Your account has been inactive. Contact VCG administrator"), fail_silently = True)
                    return HttpResponseRedirect('/admin_user/logout/')                
                if request.user.is_superuser:
                    if domain_name:
                        messages.success(request, _("Invalid Username or Password"), fail_silently = True)
                        return HttpResponseRedirect('/logout/')
                    return HttpResponseRedirect('/admin_management/company_list/')
                else:
                    user = User.objects.filter(id = request.user.id)
                    if user:
                        for g in request.user.groups.all():
                            if g.name == "COMPANY":
                                if company[0].sub_domain == domain_name:
                                    return HttpResponseRedirect('/'+domain_name+'/company_management/company_tasks/')
                                else:
                                    messages.success(request, _("Invalid Username or Password"), fail_silently = True)
                                    return HttpResponseRedirect('/admin_user/logout/')
                            elif g.name == "CAREGIVER":
                                if caregiver[0].company.sub_domain == domain_name:
                                    return HttpResponseRedirect('/'+domain_name+'/caregiver_management/caregiver_tasks/')
                                else:
                                    messages.success(request, _("Invalid Username or Password"), fail_silently = True)
                                    return HttpResponseRedirect('/admin_user/logout/')
                            elif g.name == "CLIENT":
                                if client[0].company.sub_domain == domain_name:
                                    return HttpResponseRedirect('/'+domain_name+'/client_management/client_home/')
                                else:
                                    messages.success(request, _("Invalid Username or Password"), fail_silently = True)
                                    return HttpResponseRedirect('/admin_user/logout/')
                            elif g.name == "ADMIN":
                                if domain_name:
                                    messages.success(request, _("Invalid Username or Password"), fail_silently = True)
                                    return HttpResponseRedirect('/admin_user/logout/')
                                return HttpResponseRedirect('/admin_management/company_list/')
            else:
                state = _("Your account is not active, please contact the site admin.")
        else:
            state = _("Your username and/or password were incorrect.")

    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def logout_user(request, domain_name = None):
    if not request.user or str(request.user) == 'AnonymousUser':
        if domain_name:
            return HttpResponseRedirect('/'+domain_name)
        else:
            return HttpResponseRedirect('/')
    elif request.user:
        logout(request)
        if domain_name:
            return HttpResponseRedirect('/'+domain_name)
        else:
            return HttpResponseRedirect('/')
    
def user_list(request): 
    return render_to_response('admin/user_list.html', locals(), context_instance = RequestContext(request))

def user_edit(request): 
    return render_to_response('admin/user_edit.html', locals(), context_instance = RequestContext(request))

def set_lang(request):
    lang = request.GET['lang_code']
    request.session['lang'] = lang
    json = simplejson.dumps('success')
    return HttpResponse(json, mimetype='application/javascript')

def vchat_req(request):
    if request.GET:
        receiver = request.GET.get('to')         
        
        video_session = None
        try:
            video_session = VideoSession.objects.get(sender = request.user, receiver = User.objects.get(username = receiver))
        except:
            video_session = VideoSession.objects.create(sender = request.user, receiver = User.objects.get(username = receiver))
            

        api_key         = '24175212' # Replace with your OpenTok API key.
        api_secret      = '40f335ab2eb8bcd4c5f6c4c7cfa70638c1aff011'  # Replace with your OpenTok API secret.
        session_address = request.META.get('REMOTE_ADDR') # Replace with the representative URL of your session.
        
        opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret)
        session     = opentok_sdk.create_session(session_address, {'p2p_preference':'enabled'})
        
        connectionMetadata  = 'username=' + request.user.username + ', userLevel=4'
        token               = opentok_sdk.generate_token(session.session_id, OpenTokSDK.RoleConstants.PUBLISHER, None, connectionMetadata)

        video_session.session_id    = session.session_id
        video_session.token_id      = token            
        video_session.save()
        
        session_id  = session.session_id
        token_id    = token
        message = 'VCHAT_REQ->' + request.user.username
        ChatMessage.objects.create(sender = request.user, receiver = User.objects.get(username = receiver), message = message)
        
        return render_to_response('vchat.html', locals(), context_instance=RequestContext(request))
    
def vchat_join(request):
    if request.GET:
        receiver = request.GET.get('from')         
        
        video_session = None
        try:
            video_session = VideoSession.objects.get(receiver = request.user, sender = User.objects.get(username = receiver))
        except:
            return HttpResponse ("There is request now!")
            
        video_session
        
        session_id  = video_session.session_id
        token_id    = video_session.token_id
        
        return render_to_response('vchat.html', locals(), context_instance=RequestContext(request))
