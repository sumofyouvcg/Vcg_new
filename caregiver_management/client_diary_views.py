import re

from datetime import date, timedelta
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.utilities import caregiver_login ,view_access, company_access
from vcg.admin_management.models import Client, Caregiver, DiaryQuestion, QuestionChoice, QuestionSlider
from vcg.company_management.models import ClientCaregivers, CompanyClientDiary, Messages
from vcg.company_management.client_diary_forms import CompanyClientDiaryForm
from vcg.client_management.client_diary_forms import DiaryFeedbackForm
from vcg.client_management.models import ClientDiary, DiaryFeedback
from vcg.config import choices


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
@caregiver_login
@view_access
def client_diary_list(request, domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False   
            
    diary_list = CompanyClientDiary.objects.filter(client__id = client_id).order_by('-modified_at')
    paginate  = Paginator(diary_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        diary_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        diary_list = paginate.page(paginate.num_pages)
    num_pages = range(diary_list.paginator.num_pages)
    return render_to_response('caregiver/client_diary_list.html', locals(), context_instance=RequestContext(request))

@caregiver_login
@company_access
def client_diary_add(request,domain_name = None, client_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    client = Client.objects.get(id = client_id)
    form    = CompanyClientDiaryForm(user=request.user, initial={'client': client})
    if request.POST:
        form = CompanyClientDiaryForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            diary = form.save(commit = False)
            diary.created_by = diary.modified_by = request.user
            diary.assign_status = True
            diary.save()
            ClientCaregivers.objects.create(client = diary.client , caregiver = diary.caregiver, task_id = "diary_"+str(diary.id))
            messages.success(request,(_("Diary Assigned Successfully")),
                                         fail_silently = True)
            return redirect(reverse('caregiver_client_diary_list', kwargs={'domain_name': domain_name, 'client_id':str(client_id)}))
        else:
            return render_to_response('caregiver/client_diary_add.html', locals(), context_instance = RequestContext(request))
    else:
        form    = CompanyClientDiaryForm(user=request.user, initial={'client': client_id})
    return render_to_response('caregiver/client_diary_add.html', locals(), context_instance = RequestContext(request))

@caregiver_login
@view_access
def client_diary_show(request, domain_name = None, client_id = None, diary_id = None):   
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False 
    try:        
        diary =  CompanyClientDiary.objects.get(id = diary_id)
        start_date = diary.created_at.date()
        end_date   = date.today()+ timedelta(days=1)
        client_events = """ """
        if (diary.intervel) == '0':
            for single_date in daterange(start_date, end_date):
                diary_entry =  ClientDiary.objects.filter(diary = diary, date = str(single_date))
                if diary_entry:
                    client_events += """
                                 {
                                    title: '"""+str(diary)+"""',
                                    start: new Date("""+str(single_date.year)+""","""+str((single_date.month)-1)+""","""+str(single_date.day)+"""),
                                    url:'/"""+str(domain_name)+"""/caregiver_management/client_diary_view/"""+str(client_id)+"""/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                    color: '#009966  !important', 
                                    textColor: 'white !important',
                                },
                    """
                else:
                    if str(single_date) == str(date.today()):
                        client_events += """
                                     {
                                        title: '"""+str(diary)+"""',
                                        start: new Date("""+str(single_date.year)+""","""+str((single_date.month)-1)+""","""+str(single_date.day)+"""),
                                        url:'/"""+str(domain_name)+"""/caregiver_management/client_diary_today/"""+str(client_id)+"""/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                        color: '#0099FF !important', 
                                        textColor: 'white !important',
                                    },
                        """
                    else:
                        client_events += """
                                     {
                                        title: '"""+str(diary)+"""',
                                        start: new Date("""+str(single_date.year)+""","""+str((single_date.month)-1)+""","""+str(single_date.day)+"""),
                                        url:'/"""+str(domain_name)+"""/caregiver_management/client_diary_view/"""+str(client_id)+"""/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                        color: '#CC3300 !important', 
                                        textColor: 'white !important',
                                    },
            
                        """
        else:
            for single_date in daterange(start_date, end_date):
                days = (single_date - start_date).days
                if (days % 7)==0:
                    diary_entry =  ClientDiary.objects.filter(diary = diary, date = str(single_date))
                    if diary_entry:
                        client_events += """
                                     {
                                        title: '"""+str(diary)+"""',
                                        start: new Date("""+str(single_date.year)+""","""+str((single_date.month)-1)+""","""+str(single_date.day)+"""),
                                        url:'/"""+str(domain_name)+"""/caregiver_management/client_diary_view/"""+str(client_id)+"""/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                        color: '#009966 !important', 
                                        textColor: 'white !important',                               
                                    },
            
                        """
                    else:
                        if str(single_date) == str(date.today()):
                            client_events += """
                                         {
                                            title: '"""+str(diary)+"""',
                                            start: new Date("""+str(single_date.year)+""","""+str((single_date.month)-1)+""","""+str(single_date.day)+"""),
                                            url:'/"""+str(domain_name)+"""/caregiver_management/client_diary_today/"""+str(client_id)+"""/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                            color: '#0099FF !important', 
                                            textColor: 'white !important',
                                        },
                            """
                        else:
                            client_events += """
                                         {
                                            title: '"""+str(diary)+"""',
                                            start: new Date("""+str(single_date.year)+""","""+str((single_date.month)-1)+""","""+str(single_date.day)+"""),
                                            url:'/"""+str(domain_name)+"""/caregiver_management/client_diary_view/"""+str(client_id)+"""/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                            color: '#CC3300 !important', 
                                            textColor: 'white !important',
                                        },
                
                            """
        diary_feedbacks = DiaryFeedback.objects.filter(diary = diary).exclude(created_by = request.user).order_by('-created_at')                        
        return render_to_response('caregiver/client_diary_show.html', locals(), context_instance = RequestContext(request))
    except CompanyClientDiary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_diary_list', kwargs={'domain_name': domain_name}))
    
@caregiver_login
@view_access
def client_diary_view(request, domain_name = None, client_id = None, diary_id = None, date = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    caregiver = Caregiver.objects.get(caregiver_number = request.user.username)    
    if caregiver.role == "Analyst":
        analyst = True
    else:
        analyst = False 
    try:
        diary =  CompanyClientDiary.objects.get(id = diary_id)
        exist_feedback = DiaryFeedback.objects.filter(diary = diary_id, date=date).order_by('created_at')
        client_diary_questions = ClientDiary.objects.filter(diary__id = diary_id, date = date)
        full_choices = []
        slider_val   = []
        if client_diary_questions:
            for question in client_diary_questions:
                if question.answer_options:
                    choice_options = question.answer_options.splitlines()
                    choice_value = []
                    for options in choice_options:
                        if not re.match(r'^[\s]*$', options):
                            if not (options == ''):
                                choice_value.append(options)
                    full_choices.append({'id':question.id,  'options':choice_value})
                if question.answer_type == '4':
                    slider_val.append({'id':question.id,'min_val':question.min_value, 'max_val':question.max_value})
                    
        if request.method == "POST":
            form = DiaryFeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientDiary.objects.filter(pk = diary_id, active = True).update(assign_status = True, post_status = False)
                messages.success(request,(_("Your Feedback Sent Successfully")),fail_silently = True)
                return redirect(reverse('caregiver_client_diary_show', kwargs={'domain_name': domain_name, 'client_id':str(client_id), 'diary_id':diary_id}))
            else:
                return render_to_response('caregiver/client_diary_view.html', locals(), context_instance = RequestContext(request))
    
        form = DiaryFeedbackForm()
        return render_to_response('caregiver/client_diary_view.html', locals(), context_instance = RequestContext(request))
    except CompanyClientDiary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_diary_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))
    
@caregiver_login
@view_access
def client_diary_today(request, domain_name = None, client_id = None, diary_id = None, current_date = None):   
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    try:
        diary =  CompanyClientDiary.objects.get(id = diary_id)
        all_ques = DiaryQuestion.objects.filter(diary = diary.diary) 
        slider_val=[]
        choice_val=[]    
        if all_ques:
            for ques in all_ques:
                all_choice = QuestionChoice.objects.filter(diary_question__id = ques.id,)
                new_options=[]
                if all_choice:
                    for choice in all_choice:
                        options = choice.answer.splitlines()
                        new_options=[]
                        for option in options:
                            if not re.match(r'^[\s]*$', option):
                                if not (option == ''):
                                    new_options.append(option)
                
                    choice_val.append({'ques_id':choice.diary_question.id,'answer':new_options})    
                all_slider = QuestionSlider.objects.filter(diary_question__id = ques.id)
                if all_slider:
                    for slider in all_slider:
                        slider_val.append({'ques_id':slider.diary_question.id,'min_val':slider.min_value, 'max_val':slider.max_value})
    
        question_list = DiaryQuestion.objects.filter(diary = diary.diary)
        return render_to_response('caregiver/client_diary_today.html', locals(), context_instance = RequestContext(request))
    except CompanyClientDiary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed by Company')), fail_silently= True)
        return redirect(reverse('caregiver_client_diary_list', kwargs={'domain_name': domain_name}))
    
@caregiver_login
@company_access
def client_diary_edit(request, domain_name = None, client_id = None, diary_id = None):
    client = Client.objects.get(id = client_id)
    client_user = User.objects.get(username = client.client_number)
    new_messages  = len(Messages.objects.filter(created_by = client_user, recipient = request.user, read_status = False))
    
    try:
        diary = CompanyClientDiary.objects.get(pk = diary_id)
        selected_diary = get_object_or_404(CompanyClientDiary, pk = diary_id)
        if request.POST:
            form = CompanyClientDiaryForm(request.POST, request.FILES,instance = selected_diary, user=request.user)
            if form.is_valid():
                diary = form.save(commit = False)
                diary.created_by = diary.modified_by = request.user
                diary.assign_status = True
                diary.save()
                ClientCaregivers.objects.filter(client = diary.client ,task_id = "diary_"+str(diary.id)).delete()
                ClientCaregivers.objects.create(client = diary.client , caregiver = diary.caregiver, task_id = "diary_"+str(diary.id), created_by = request.user, modified_by = request.user)
                messages.success(request,(_("Diary Edited Successfully")),fail_silently = True)
                return redirect(reverse('caregiver_client_diary_show', kwargs={'domain_name': domain_name, 'client_id':client_id, 'diary_id':diary_id}))
            else:
                return render_to_response('caregiver/client_diary_edit.html', locals(), context_instance=RequestContext(request))
        else:
            form = CompanyClientDiaryForm(user=request.user, instance = selected_diary)
        return render_to_response('caregiver/client_diary_edit.html', locals(), context_instance=RequestContext(request))
    except CompanyClientDiary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed by Admin')), fail_silently= True)
        return redirect(reverse('caregiver_client_diary_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))
    
@caregiver_login
@company_access
def client_diary_delete(request, domain_name = None, client_id = None):
    if request.method == 'POST':
        company_client_diary_ids    = request.POST.getlist('choices')
        for company_client_diary_id in company_client_diary_ids:
            diary = CompanyClientDiary.objects.get(id = company_client_diary_id)
            diary.delete()
        if len(company_client_diary_ids) > 1:
            messages.success(request,(_("Selected Diaries Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Diary Deleted Successfully")),fail_silently = True)
    return redirect(reverse('caregiver_client_diary_list', kwargs={'domain_name': domain_name, 'client_id':client_id}))