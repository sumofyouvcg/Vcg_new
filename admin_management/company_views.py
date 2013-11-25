from datetime import date

from vcg.admin_management.company_forms import CompanyForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Module, CompanyModules, Company, Caregiver, Client, TestModule, Test, MailConfiguration
from vcg.admin_management.client_forms import ClientForm
from vcg.admin_management.caregivers_forms import CaregiversForm
from vcg.config import default_groups, mail, choices
from vcg.utilities import Utility, admin_login, Email, permission_view
from vcg.settings import SERVER_DOMAIN_URL

@admin_login
@permission_view('COMP1', None)
def company_add(request, read_only):
    print "=" * 50
    print request.LANGUAGE_CODE
    print "=" * 50
    domain_url = SERVER_DOMAIN_URL
    currentdate = date.today()
    if request.POST:
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit = False)
            company.created_by = company.modified_by = request.user
#            if company.from_date > currentdate:
#                company.active = False
            company.save()
            current_company = company.id
# For User Mgnt            
            random_password = Utility().generate_password()
            auth_user = User.objects.create_user(company.company_number, company.email, random_password)
            auth_user.is_active = company.active
            auth_user.is_staff = company.active
            auth_user.first_name = company.company_name
            default_groups.COMPANY = Group.objects.get(pk = 2)
            auth_user.groups = list(auth_user.groups.all()) + [default_groups.COMPANY, ]
            auth_user.save()
            mail_config = MailConfiguration.objects.filter()
# For Mail Diffrentiation            
            if mail_config:
                if company.language == 'English':
                    creation_subject = mail.CREATION_SUBJECT_ENGLISH
                    creation_message = mail.DEAR_ENGLISH %(company.company_name)+str(mail_config[0])+mail.USER_DETAILS_ENGLISH %(company.sub_domain, company.company_number, random_password)
                else:
                    creation_subject = mail.CREATION_SUBJECT_DUTCH
                    creation_message = mail.DEAR_DUTCH %(company.company_name)+str(mail_config[0])+mail.USER_DETAILS_DUTCH %(company.sub_domain, company.company_number, random_password)
            else:
                creation_subject = mail.USER_CREATION_SUBJECT
                creation_message = mail.DEAR_ENGLISH %(company.company_name)+mail.USER_DETAILS_ENGLISH %(company.sub_domain, company.company_number, random_password)
            Email().send_email(creation_subject, creation_message, [company.email], "html")
            
            if company.active:
                Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_ACTIVATION_MSG %(company.company_name), [company.email], "html")
            return redirect('/admin_management/company_modules/'+str(current_company)+"/")
        else:
            return render_to_response('admin/company_add.html', locals(), context_instance=RequestContext(request))
    else:
        form = CompanyForm()
    return render_to_response('admin/company_add.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('COMP3', None)
def company_list(request,read_only, comp_id = None):
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        companylist = Company.objects.filter(Q(company_name__icontains = key)|Q(company_number__icontains = key)|Q(email__icontains = key)|Q(phone_number__icontains = key)|Q(address__icontains = key)|Q(zip_code__icontains = key)|Q(place_name__icontains = key)).order_by('-modified_at')
    else:
        companylist = Company.objects.all().order_by('-modified_at')
    
    paginate  = Paginator(companylist, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        companylist = paginate.page(page)
    except (EmptyPage, InvalidPage):
        companylist = paginate.page(paginate.num_pages)
    num_pages = range(companylist.paginator.num_pages)
    
    return render_to_response('admin/company_list.html', locals(), context_instance=RequestContext(request))
    
@admin_login
@permission_view('COMP2', 'COMP3')
def company_edit(request, read_only, company_id = None):
    domain_url = SERVER_DOMAIN_URL
    try:
        try_company = Company.objects.get(pk = company_id)
        selected_company = get_object_or_404(Company, pk = company_id)
        old_email = selected_company.email
        currentdate = date.today()
        if request.POST:
            form = CompanyForm(request.POST, request.FILES,instance = selected_company)
            if form.is_valid():
                company = form.save(commit = False)
                company.created_by = company.modified_by = request.user
    #            if company.from_date > currentdate:
    #                company.active = False
                company.save()
                User.objects.filter(username = company.company_number).update(first_name = company.company_name)
                if old_email != company.email:
                    User.objects.filter(email = old_email).update(username = company.company_number, email = company.email)
                    Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_EDIT_MSG %(company.company_name, company.sub_domain, company.company_number), [company.email], "html")
                messages.success(request, (_("Company edited Successfully")),
                                             fail_silently = True)
                return redirect('/admin_management/company_list')
            else:
                return render_to_response('admin/company_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = CompanyForm(instance = selected_company)
        return render_to_response('admin/company_edit.html', locals(), context_instance=RequestContext(request))
    except Company.DoesNotExist:
        messages.success(request, (_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
    
@admin_login
@permission_view('COMP4')
def company_delete(request, read_only):
    if request.method == 'POST':
        company_ids     = request.POST.getlist('choices')
        for company_id in company_ids:
            company     = Company.objects.get(id = company_id)

            caregivers  = Caregiver.objects.filter(company = company)
            for caregiver in caregivers:
                User.objects.filter(username = caregiver.caregiver_number).delete()

            clients     = Client.objects.filter(company = company)
            for client in clients:
                User.objects.filter(username = client.client_number).delete()

            User.objects.filter(username = company.company_number).delete()
            company.delete()
        if len(company_ids) > 1:
            messages.success(request, (_("Selected Companies Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Company Deleted Successfully")),fail_silently = True)        
    return redirect('/admin_management/company_list/')

@admin_login
@permission_view('COMP2', 'COMP3')
def company_caregivers(request, read_only, company_id = None):
    
    try:
        try_company = Company.objects.get(pk = company_id)
        comp_active = Company.objects.filter(id = company_id, active =True)
        key = request.GET.get('keyword')
        filter_val = request.GET.get('filter')
        
        if filter_val:
            if filter_val=="InActive":
                caregiver_list = Caregiver.objects.filter(active = False, company = company_id).order_by('-modified_at')
            elif filter_val == "All":    
                caregiver_list = Caregiver.objects.filter(active = True, company = company_id).order_by('-modified_at')
        if key is not None: 
            key = key.lstrip()
        if key :
            caregiver_list = Caregiver.objects.filter(Q(name__icontains = key)|Q(caregiver_number__icontains = key)|Q(email__icontains = key)|Q(place_name__icontains = key)|Q(zip_code__icontains = key)|Q(address__icontains = key)|Q(phone_number__icontains = key), company = company_id).order_by('-modified_at')
        
        if not filter_val and not key:
            caregiver_list = Caregiver.objects.filter(company = company_id).order_by('-modified_at')
        
        paginate  = Paginator(caregiver_list, choices.list_per_page)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
    
        try:
            caregiver_list = paginate.page(page)
        except (EmptyPage, InvalidPage):
            caregiver_list = paginate.page(paginate.num_pages)
        num_pages = range(caregiver_list.paginator.num_pages) 
        
        return render_to_response('admin/company_caregivers.html', locals(), context_instance=RequestContext(request))
    except Company.DoesNotExist:
        messages.success(request,(_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
@admin_login
@permission_view('COMP2','COMP3')
def company_client(request,read_only, company_id = None):
    
    try:
        try_company = Company.objects.get(pk = company_id)
        comp_active = Company.objects.filter(id = company_id, active =True)
        key = request.GET.get('keyword')
        filter_val = request.GET.get('filter')
        if filter_val:
            if filter_val=="InActive":
                client_list = Client.objects.filter(active = False, company = company_id).order_by('-modified_at')
            elif filter_val == "All":    
                client_list = Client.objects.filter(active = True, company = company_id).order_by('-modified_at')
        if key is not None: 
            key = key.lstrip()
        if key :
            client_list = Client.objects.filter(Q(name__icontains = key)|Q(client_number__icontains = key)|Q(email__icontains = key)|Q(place_name__icontains = key)|Q(zip_code__icontains = key)|Q(address__icontains = key)|Q(phone_number__icontains = key), company = company_id).order_by('-modified_at')
    
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
        return render_to_response('admin/company_client.html', locals(), context_instance=RequestContext(request))
    except Company.DoesNotExist:
        messages.success(request,(_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
@admin_login
@permission_view('COMP1',None)
def company_modules(request, read_only,comp_id = None):
    modules = Module.objects.filter(active = True)
    test_list = Test.objects.filter(active = True)
    module_error = test_error = ""
    if request.POST:
        selected_modules = request.POST.getlist('choices')
        selected_tests   = request.POST.getlist('tchoices')
        if selected_modules and selected_tests:
            for selected in selected_modules:
                check = Module.objects.get(id = selected)
                company = Company.objects.get(id = comp_id)
                register_modules = CompanyModules(company = company,
                                                    modules = check,
                                                    created_by = request.user,
                                                    modified_by = request.user)
                register_modules.save()
            for selected in selected_tests:
                check = Test.objects.get(id = selected)
                company = Company.objects.get(id = comp_id)
                register_modules = TestModule(company = company,
                                                    tests = check,
                                                    created_by = request.user,
                                                    modified_by = request.user)
                register_modules.save()
            messages.success(request,("Company Saved Successfully"),
                                         fail_silently = True) 
            return redirect('/admin_management/company_list/')
        else:
            if not selected_modules:
                module_error = _('Choose atleast one module')
            if not selected_tests:
                test_error = _('Choose atleast one module')
    return render_to_response('admin/company_modules.html', locals(), context_instance=RequestContext(request))


@admin_login
@permission_view('COMP2', None)
def company_add_caregiver(request,read_only, company_id = None):
    try:
        comp = Company.objects.get(id = company_id)
        form    = CaregiversForm( initial={'company': comp})
        if request.POST:
            form = CaregiversForm(request.POST, request.FILES)
            if form.is_valid():
                caregiver = form.save(commit = False)
                caregiver.created_by = caregiver.modified_by = request.user
                caregiver.save()
                # For User Mgnt            
                random_password = Utility().generate_password()
                auth_user = User.objects.create_user(caregiver.caregiver_number, caregiver.email, random_password)
                auth_user.is_active = True
                auth_user.is_staff = True
                auth_user.first_name = caregiver.name
                default_groups.CAREGIVER = Group.objects.get(pk = 3)
                auth_user.groups = list(auth_user.groups.all()) + [default_groups.CAREGIVER, ]
                auth_user.save()
                Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_CREATION_MSG %(caregiver.name, caregiver.company.sub_domain, caregiver.caregiver_number, random_password), [caregiver.email], "html")
                messages.success(request,(_("Caregiver Saved Successfully")),
                                             fail_silently = True)
                return redirect('/admin_management/company_caregivers/'+company_id+'/')
            else:
                return render_to_response('admin/company_add_caregiver.html', locals(), context_instance=RequestContext(request))
        else:
            form = CaregiversForm(initial={'company': company_id})
        return render_to_response('admin/company_add_caregiver.html', locals(), context_instance=RequestContext(request))
    except Company.DoesNotExist:
        messages.success(request,(_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
@admin_login
@permission_view('COMP2', 'COMP3')
def company_edit_caregiver(request,read_only, company_id = None, caregiver_id = None): 
    try:
        try_company = Company.objects.get(id = company_id)
        selected_caregiver = get_object_or_404(Caregiver, pk = caregiver_id, company = company_id)
        old_email = selected_caregiver.email
        if request.POST:
            form = CaregiversForm(request.POST, request.FILES,instance = selected_caregiver)
            if form.is_valid():
                caregiver = form.save(commit = False)
                caregiver.created_by = caregiver.modified_by = request.user
                if not form.files:
                    caregiver.caregiver_image = ''
                caregiver.save()
                User.objects.filter(username = caregiver.caregiver_number).update(first_name = caregiver.name)
                if old_email != caregiver.email:
                    User.objects.filter(email = old_email).update(username = caregiver.caregiver_number, email = caregiver.email)
                    Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_EDIT_MSG %(caregiver.name, caregiver.company.sub_domain, caregiver.caregiver_number), [caregiver.email], "html")
                messages.success(request,(_("Caregiver edited Successfully")),
                                             fail_silently = True)
                return redirect('/admin_management/company_caregivers/'+company_id+'/')
            else:
                return render_to_response('admin/company_add_caregiver.html', locals(), context_instance=RequestContext(request))
        else:
            form = CaregiversForm(instance = selected_caregiver)
        return render_to_response('admin/company_add_caregiver.html', locals(), context_instance=RequestContext(request))
    except Company.DoesNotExist:
        messages.success(request, (_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
    
@permission_view('COMP4')
def company_delete_caregiver(request, read_only, company_id = None):
    try:
        try_company = Company.objects.get(id = company_id)
        if request.method == 'POST':
            company_caregiver_ids    = request.POST.getlist('choices')
            for company_caregiver_id in company_caregiver_ids:
                company_caregiver = Caregiver.objects.get(id = company_caregiver_id)
                User.objects.filter(username = company_caregiver.caregiver_number).delete()
                company_caregiver.delete()
            if len(company_caregiver_ids) > 1:
                messages.success(request, (_("Selected Caregivers Deleted Successfully")), fail_silently = True)
            else:    
                messages.success(request, (_("Selected Caregiver Deleted Successfully")), fail_silently = True)            
        return redirect('/admin_management/company_caregivers/'+company_id+'/')  
    except Company.DoesNotExist:
        messages.success(request,('This Company has been removed'), fail_silently= True)
        return redirect('/admin_management/company_list/')
    
@admin_login
@permission_view('COMP2', None)
def company_add_client(request, read_only,company_id = None):
    try:
        try_company = Company.objects.get(id = company_id)
        if request.POST:
            form = ClientForm(request.POST, request.FILES)
            if form.is_valid():
                comp             = Company.objects.get(id = company_id)  
                no_of_client     = Client.objects.filter(company = comp)
                currentdate = date.today()
                if len(no_of_client) >= comp.number_of_clients:
                    messages.success(request, (_("You are authorised to add %s Clients Only") % str(comp.number_of_clients)), fail_silently = True)
                    return redirect('/admin_management/company_client/'+company_id+'/')
                if comp.expiry_date < currentdate :
                    messages.success(request,(_("Client could not be added. This Company already expired")), fail_silently = True)
                    return redirect('/caregiver_management/client_list/')
                            
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
                messages.success(request, (_("Client Saved Successfully")),
                                             fail_silently = True)            
                
                return redirect('/admin_management/company_client/'+company_id+'/')
            else:
                return render_to_response('admin/company_add_client.html', locals(), context_instance=RequestContext(request))
        else:
            form = ClientForm()
        return render_to_response('admin/company_add_client.html', locals(), context_instance=RequestContext(request))
    except Company.DoesNotExist:
        messages.success(request,(_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
    
@admin_login
@permission_view('COMP2', 'COMP3')
def company_edit_client(request,read_only, company_id = None, client_id = None): 
    try:
        try_company = Company.objects.get(id = company_id)
        selected_client = get_object_or_404(Client, pk = client_id, company = company_id)
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
                messages.success(request,(_("Client Edited Successfully")),
                                             fail_silently = True)      
                return redirect('/admin_management/company_client/'+company_id+'/')
            else:
                return render_to_response('admin/company_add_client.html', locals(), context_instance=RequestContext(request))
        else:
            form = ClientForm(instance = selected_client)
        return render_to_response('admin/company_add_client.html', locals(), context_instance=RequestContext(request))
    except Company.DoesNotExist:
        messages.success(request,(_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
    
@admin_login
@permission_view('COMP4')
def company_delete_client(request, read_only, company_id = None):
    try:
        try_company = Company.objects.get(id = company_id)
        if request.method == 'POST':
            company_client_ids    = request.POST.getlist('choices')
            for company_client_id in company_client_ids:
                company_client = Client.objects.get(id = company_client_id)
                User.objects.filter(username = company_client.client_number).delete()
                company_client.delete()
            if len(company_client_ids) > 1:
                messages.success(request,(_("Selected Clients Deleted Successfully")),fail_silently = True)
            else:    
                messages.success(request,(_("Selected Client Deleted Successfully")),fail_silently = True)            
        return redirect('/admin_management/company_client/'+company_id+'/')   
    except Company.DoesNotExist:
        messages.success(request,(_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
    
@admin_login
@permission_view('COMP2', 'COMP3')
def company_add_modules(request, read_only,company_id = None):
    select = request.GET.get('query')
    testing = request.GET.get('tests')
    if select:
        permissions = select.split(",")
    if testing:
        test_select = testing.split(",")
    try:
        try_company = Company.objects.get(pk = company_id)
        modules = Module.objects.filter(active = True)
        test_list = Test.objects.filter(active = True)
        choosen_module = CompanyModules.objects.filter(company__id = company_id)
        test_module = TestModule.objects.filter(company__id = company_id)
        list=[]
        test = []
        module_error = test_error = ""
        for chosen in choosen_module:
            list.append(chosen.modules.id)
        for module in test_module:
            test.append(module.tests.id)
        if request.POST:
            selected_modules    = request.POST.getlist('choices')
            selected_tests    = request.POST.getlist('tchoices')
            if selected_modules and selected_tests:
                company = Company.objects.get(id = company_id)
    #For Company Modules
                current_modules = CompanyModules.objects.filter(company__id = company_id)
                cur_modules = []
                for current in current_modules:
                    cur_modules.append(str(current.modules.id))
                if current_modules:
                    for new in selected_modules:
                        if new not in cur_modules:
                            check = Module.objects.get(id = new)
                            company = Company.objects.get(id = company_id)
                            register_modules = CompanyModules(company = company,
                                                            modules = check,
                                                            created_by = request.user,
                                                            modified_by = request.user)
                            register_modules.save()
                    new_modules_list = CompanyModules.objects.filter(company__id = company_id)
                    for remove in new_modules_list:
                        if str(remove.modules.id) not in selected_modules:
                            company = CompanyModules.objects.filter(company__id = company_id, modules = remove.modules.id).delete()
                        
                else:
                    for selected in selected_modules:
                        check = Module.objects.get(id = selected)
                        company = Company.objects.get(id = company_id)
                        register_modules = CompanyModules(company = company,
                                                            modules = check,
                                                            created_by = request.user,
                                                            modified_by = request.user)
                        register_modules.save()
    # For Test Modules
                test_modules = TestModule.objects.filter(company__id = company_id)
                testing_modules = []
                for testing in test_modules:
                    testing_modules.append(str(testing.tests.id))
                if test_modules:
                    for test in selected_tests:
                        if test not in testing_modules:
                            check = Test.objects.get(id = test)
                            company = Company.objects.get(id = company_id)
                            register_modules = TestModule(company = company,
                                                            tests = check,
                                                            created_by = request.user,
                                                            modified_by = request.user)
                            register_modules.save()
                    new_tests_list = TestModule.objects.filter(company__id = company_id)
                    for remove in new_tests_list:
                        if str(remove.tests.id) not in selected_tests:
                            company = TestModule.objects.filter(company__id = company_id, tests = remove.tests.id).delete()
                        
                else:
                    for selected in selected_tests:
                        check = Test.objects.get(id = selected)
                        company = Company.objects.get(id = company_id)
                        register_modules = TestModule(company = company,
                                                            tests = check,
                                                            created_by = request.user,
                                                            modified_by = request.user)
                        register_modules.save()
                messages.success(request,(_("Modules Edited Successfully")),
                                             fail_silently = True) 
                return redirect('/admin_management/company_list/')
            else:
                if not selected_modules:
                    module_error = _('Choose atleast one module')
                if not selected_tests:
                    test_error = 'Choose atleast one module'
    except Company.DoesNotExist:
        messages.success(request,(_('This Company has been removed')), fail_silently= True)
        return redirect('/admin_management/company_list/')
    return render_to_response('admin/company_add_modules.html', locals(), context_instance=RequestContext(request))
