from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, HttpResponseRedirect

from vcg.admin_management.models import AdminUserPermission, Caregiver, Company, Client

class Utility:
    
    def __init__(self):
        return;
        
    def generate_password(self):
        """
        Generate password for users
        """
        return UserManager().make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    
    def validate_integer_field(self, value):
        if len(str(value)) >= 10:
            raise ValidationError(u'Ensure that there are no more than 9 digits in total.')
    
class Email:
    def __init__(self):
        return;

    def send_email(self, subject, message, recipients, contenttype = 'plain', attach = ''):
        try:
            from django.core.mail import EmailMessage
            from vcg.settings.base import EMAIL_HOST_USER
        finally:
            emailMessage = EmailMessage (subject, message, EMAIL_HOST_USER, recipients)
            emailMessage.content_subtype = contenttype
            if attach.strip() != '':
                emailMessage.attach_file(attach)
            emailMessage.send()

def caregiver_login(fn):    
    def decorator(request, **kwargs):
        domain_name = (request.get_full_path()).split("/")[1]
        if request.user.id:
            if request.user.is_superuser:
                messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                return HttpResponseRedirect('/admin_management/company_list/')
            else:
                user = User.objects.filter(id = request.user.id)
                if user:
                    for g in request.user.groups.all():
                        if g.name == "COMPANY":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/'+domain_name+'/company_management/company_tasks/')
                        elif g.name == "CAREGIVER":
                            caregiver = Caregiver.objects.filter(caregiver_number = request.user.username)
                            if caregiver[0].company.sub_domain == domain_name:
                                return fn(request, **kwargs)
                            else:
                                messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                                return HttpResponseRedirect('/'+domain_name+'/logout/')  
                        elif g.name == "CLIENT":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/'+domain_name+'/client_management/client_home/')
                        elif g.name == "ADMIN":
                            return fn(request, **kwargs)
        else:
            messages.success(request,("Sorry,You don't have permissions for access, Please login again"), fail_silently = True)
            return redirect('/')
        return fn(request, **kwargs)
    return decorator

def company_login(fn):    
    def decorator(request, **kwargs):
        domain_name = (request.get_full_path()).split("/")[1]
        if request.user.id:
            if request.user.is_superuser:
                messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                return HttpResponseRedirect('/admin_management/company_list/')
            else:
                user = User.objects.filter(id = request.user.id)
                if user:
                    for g in request.user.groups.all():
                        if g.name == "COMPANY":
                            company = Company.objects.filter(company_number = request.user.username)
                            if company[0].sub_domain == domain_name:
                                return fn(request, **kwargs)
                            else:
                                messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                                return HttpResponseRedirect('/'+domain_name+'/logout/')   
                        elif g.name == "CAREGIVER":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/'+domain_name+'/caregiver_management/caregiver_tasks/')
                        elif g.name == "CLIENT":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/'+domain_name+'/client_management/client_home/')
                        elif g.name == "ADMIN":
                            return fn(request, **kwargs)
        else:
            messages.success(request,("Sorry,You don't have permissions for access, Please login again"), fail_silently = True)
            return redirect('/')
        return fn(request, **kwargs)
    return decorator

def admin_login(fn):    
    def decorator(request, **kwargs):
        if request.user.id:
            if request.user.is_superuser:
                return fn(request, **kwargs)
            else:
                user = User.objects.filter(id = request.user.id)
                if user:
                    for g in request.user.groups.all():
                        if g.name == "COMPANY":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/company_management/company_tasks/')
                        elif g.name == "CAREGIVER":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/caregiver_management/caregiver_tasks/')
                        elif g.name == "CLIENT":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/client_management/client_home/')
                        elif g.name == "ADMIN":
                            return fn(request, **kwargs)
        else:
            messages.success(request,("Sorry,You don't have permissions for access, Please login again"), fail_silently = True)
            return redirect('/')
        return fn(request, **kwargs)
    return decorator

def permission_view(msg = 'my default message', alt = "none"):
    def decorator(func):
        def newfn(request, **kwargs):
            if not request.user.is_superuser:
                auth_views = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file
                if (msg in auth_views) or (request.user.is_superuser) or (str(alt) in auth_views):
                    if not msg in auth_views:
                        kwargs['read_only'] = "readonly"
                    else:
                        kwargs['read_only'] = ""
                    return func(request, **kwargs)
                else:
                    messages.success(request,("Sorry,You don't have permissions for access, Please login again"), fail_silently = True)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
            kwargs['read_only'] = ""
            return func(request, **kwargs)
        return newfn
    return decorator

def view_access(fn):
    def decorator(request, **kwargs):
        caregiver_name = Caregiver.objects.get(caregiver_number = request.user.username)
        if caregiver_name.role == 'Analyst' or caregiver_name.role == 'Company':
            return fn(request, **kwargs)
        else:
            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
            return HttpResponseRedirect('/'+caregiver_name.company.sub_domain+'/caregiver_management/caregiver_tasks/')
    return decorator

def company_access(fn):    
    def decorator(request, **kwargs):
        caregiver_name = Caregiver.objects.get(caregiver_number = request.user.username)
        if caregiver_name.role == 'Analyst':
            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        elif caregiver_name.role == 'Company':
            return fn(request, **kwargs)
        else:
            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
            return HttpResponseRedirect('/'+caregiver_name.company.sub_domain+'/caregiver_management/caregiver_tasks/')
    return decorator

def client_login(fn):    
    def decorator(request, **kwargs):
        domain_name = (request.get_full_path()).split("/")[1]
        if request.user.id:
            if request.user.is_superuser:
                messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                return HttpResponseRedirect('/admin_management/company_list/')
            else:
                user = User.objects.filter(id = request.user.id)
                if user:
                    for g in request.user.groups.all():
                        if g.name == "COMPANY":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/'+domain_name+'/company_management/company_tasks/')
                        elif g.name == "CAREGIVER":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/'+domain_name+'/caregiver_management/caregiver_tasks/')
                        elif g.name == "CLIENT":
                            client = Client.objects.filter(client_number = request.user.username)
                            if client[0].company.sub_domain == domain_name:
                                return fn(request, **kwargs)
                            else:
                                messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                                return HttpResponseRedirect('/'+domain_name+'/logout/')  
                            return fn(request, **kwargs)    
                        elif g.name == "ADMIN":
                            messages.success(request,("Sorry,You don't have access permissions  "), fail_silently = True)
                            return HttpResponseRedirect('/')
        else:
            messages.success(request,("Sorry,You don't have permissions for access, Please login again"), fail_silently = True)
            return redirect('/')
        return fn(request, **kwargs)
    return decorator