import re 
import datetime

from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import date, timedelta
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Client, DiaryQuestion, QuestionChoice, QuestionSlider
from vcg.company_management.models import CompanyClientDiary
from vcg.client_management.client_diary_forms import DiaryFeedbackForm
from vcg.client_management.models import ClientDiary, DiaryFeedback
from vcg.utilities import client_login
from vcg.config import choices

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
@client_login
def diary_list(request, domain_name = None):  
    diary_list =  CompanyClientDiary.objects.filter(client__client_number = request.user.username)

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
    return render_to_response('client/client_diary_list.html', locals(), context_instance = RequestContext(request))


@client_login
def diary_show(request, domain_name = None, diary_id = None):   
    CompanyClientDiary.objects.filter(id = diary_id).update(assign_status = False)
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
                                    url:'/"""+str(domain_name)+"""/client_management/diary_view_details/"""+str(diary.id)+"""/"""+str(single_date)+"""',
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
                                        url:'/"""+str(domain_name)+"""/client_management/diary_view/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                        color: '#0099FF !important', 
                                        textColor: 'white !important',
                                    },
                        """
                    else:
                        client_events += """
                                     {
                                        title: '"""+str(diary)+"""',
                                        start: new Date("""+str(single_date.year)+""","""+str((single_date.month)-1)+""","""+str(single_date.day)+"""),
                                        url:'/"""+str(domain_name)+"""/client_management/diary_view_details/"""+str(diary.id)+"""/"""+str(single_date)+"""',
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
                                        url:'/"""+str(domain_name)+"""/client_management/diary_view_details/"""+str(diary.id)+"""/"""+str(single_date)+"""',
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
                                            url:'/"""+str(domain_name)+"""/client_management/diary_view/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                            color: '#0099FF !important', 
                                            textColor: 'white !important',
                                        },
                            """
                        else:
                            client_events += """
                                         {
                                            title: '"""+str(diary)+"""',
                                            start: new Date("""+str(single_date.year)+""","""+str((single_date.month)-1)+""","""+str(single_date.day)+"""),
                                            url:'/"""+str(domain_name)+"""/client_management/diary_view_details/"""+str(diary.id)+"""/"""+str(single_date)+"""',
                                            color: '#CC3300 !important', 
                                            textColor: 'white !important',
                                        },
                
                            """
        diary_feedbacks = DiaryFeedback.objects.filter(diary = diary).exclude(created_by = request.user).order_by('-created_at')                        
        return render_to_response('client/diary_show.html', locals(), context_instance = RequestContext(request))
    except CompanyClientDiary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_diary_list', kwargs={'domain_name': domain_name }))
    
@client_login
def diary_view(request, domain_name = None, diary_id = None, current_date = None):   
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
        if request.POST:
            error_list=[]
            answer_list=[]
            for total in request.POST:
                if 'text' in total or 'radio' in total or 'checkbox' in total or 'slider' in total:
                    for question in question_list:   
                        textquestion = 'text'+str(question.id)
                        radioquestion = 'radio'+str(question.id)
                        checkquestion = 'checkbox'+str(question.id)
                        sliderquestion = 'slider'+str(question.id)
                        if textquestion == total or radioquestion == total or checkquestion == total or sliderquestion == total:
                            if textquestion == total:
                                questions = request.POST.get(textquestion)
                            elif radioquestion == total:
                                questions = request.POST.get(radioquestion)
                            elif checkquestion == total:
                                questions = request.POST.getlist(checkquestion)
                            elif sliderquestion == total:
                                questions = request.POST.get(sliderquestion)
                            
                            question = DiaryQuestion.objects.get(id = question.id)
                            diary_assign = CompanyClientDiary.objects.get(id = diary_id)
                            if question.answer_type == '2' or question.answer_type == '3':
                                question_choice = QuestionChoice.objects.get(diary_question = question)
                                ClientDiary.objects.create(client_question_id           = question.id,
                                                                      diary             = diary_assign,
                                                                      question          =  question.question,
                                                                      help_text         = question.help_text,
                                                                      answer_type       = question.answer_type,
                                                                      exact_answer      = questions,
                                                                      answer_options    = question_choice.answer,
                                                                      date              = date.today(),
                                                                      created_by        = request.user,
                                                                      modified_by       = request.user,
                                                                      )
                            elif question.answer_type == '4':
                                question_slider = QuestionSlider.objects.get(diary_question = question)
                                ClientDiary.objects.create(client_question_id           = question.id,
                                                                      diary             = diary_assign,
                                                                      question          =  question.question,
                                                                      help_text         = question.help_text,
                                                                      answer_type       = question.answer_type,
                                                                      exact_answer      = questions,
                                                                      min_value         = question_slider.min_value,
                                                                      max_value         = question_slider.max_value,
                                                                      date              = date.today(),
                                                                      created_by        = request.user,
                                                                      modified_by       = request.user,
                                                                      )
                            else:
                                ClientDiary.objects.create(client_question_id           = question.id,
                                                                      diary             = diary_assign,
                                                                      question          =  question.question,
                                                                      help_text         = question.help_text,
                                                                      answer_type       = question.answer_type,
                                                                      exact_answer      = questions,
                                                                      date              = date.today(),
                                                                      created_by        = request.user,
                                                                      modified_by       = request.user,
                                                                      )
            CompanyClientDiary.objects.filter(id = diary_id).update(post_status = True, post_read_status = True)
            messages.success(request,(_("Diary Saved Successfully")),
                                             fail_silently = True)
            return redirect(reverse('client_diary_list', kwargs={'domain_name': domain_name }))
    
    
        return render_to_response('client/diary_view.html', locals(), context_instance = RequestContext(request))
    except CompanyClientDiary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_diary_list', kwargs={'domain_name': domain_name }))

@client_login
def diary_view_details(request, domain_name = None, diary_id = None, date = None):
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
                
                CompanyClientDiary.objects.filter(id = diary_id).update(assign_status = False, post_status = True, post_read_status = True)
                messages.success(request,(_("Your Feedback Sent Successfully")),fail_silently = True)
                return redirect(reverse('client_diary_show', kwargs={'domain_name': domain_name, 'diary_id':diary_id }))
            else:
                return render_to_response('client/diary_view_details.html', locals(), context_instance = RequestContext(request))
    
        form = DiaryFeedbackForm()
        return render_to_response('client/diary_view_details.html', locals(), context_instance = RequestContext(request))
    except CompanyClientDiary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_diary_list', kwargs={'domain_name': domain_name }))
    
def webcam(request, domain_name = None):   
    
    return render_to_response('client/webcam.html', locals(), context_instance = RequestContext(request))

def chat(request, domain_name = None):   
    
    return render_to_response('client/chat.html', locals(), context_instance = RequestContext(request))

def add_chat(request, domain_name = None):   
    
    return render_to_response('client/add_chat.html', locals(), context_instance = RequestContext(request))
