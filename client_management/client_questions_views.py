import re

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext as _

from vcg.client_management.models import ClientQuestions, ClientQuestionsFeedback, ClientQuestionsAnswers
from vcg.client_management.client_question_forms import  ClientQuestionsFeedbackForm
from vcg.admin_management.models import CreateQuestion, CreateQuestionChoice, CreateQuestionSlider, Client
from vcg.company_management.models import CompanyClientTreatment
from vcg.utilities import client_login
from vcg.config import choices

@client_login
def questions_list(request, domain_name = None):   
    client_name = Client.objects.get(client_number = request.user)
    client_questions = CompanyClientTreatment.objects.filter(client = client_name, active = True)
    paginate  = Paginator(client_questions, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        client_questions = paginate.page(page)
    except (EmptyPage, InvalidPage):
        client_questions = paginate.page(paginate.num_pages)
    num_pages = range(client_questions.paginator.num_pages)
    return render_to_response('client/questions_list.html', locals(), context_instance = RequestContext(request))

@client_login
def client_question_view(request, domain_name = None, treat_id = None):
    client_name = Client.objects.get(client_number = request.user.username) 
    
    CompanyClientTreatment.objects.filter(client__id = client_name.id, id = treat_id, active = True).update(question_active_status = False)
    try:
        question = CompanyClientTreatment.objects.get(client__id = client_name.id, id = treat_id, active = True)
        client_questions = ClientQuestions.objects.filter(client__client_number = request.user.username, question__module__id = question.module.id)
        if client_questions:
            return redirect(reverse('client_question_feedback', kwargs={'domain_name': domain_name, 'module_id':treat_id}))
        slider_val=[]
        choice_val=[]
        all_ques = CreateQuestion.objects.filter(module = question.module)
        if all_ques:
            for ques in all_ques:
                all_choice = CreateQuestionChoice.objects.filter(create_question__id = ques.id,)
                new_options=[]
                if all_choice:
                    for choice in all_choice:
                        options = choice.answer.splitlines()
                        new_options=[]
                        for option in options:
                            if not re.match(r'^[\s]*$', option):
                                if not (option == ''):
                                    new_options.append(option)
                
                    choice_val.append({'ques_id':choice.create_question.id,'answer':new_options})    
                all_slider = CreateQuestionSlider.objects.filter(create_question__id = ques.id)
                if all_slider:
                    for slider in all_slider:
                        slider_val.append({'ques_id':slider.create_question.id,'min_val':slider.min_value, 'max_val':slider.max_value})
        question_list = CreateQuestion.objects.filter(module = question.module)
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
                            
                            question = CreateQuestion.objects.get(id = question.id)
                            module_assign = CompanyClientTreatment.objects.get(client = client_name, id = treat_id)
                            if question.answer_type == '2' or question.answer_type == '3':
                                question_choice = CreateQuestionChoice.objects.get(create_question = question)
                                ClientQuestionsAnswers.objects.create(client_question_id = question.id,
                                                                      module = module_assign,
                                                                      question_text =  question.question_text,
                                                                      help_text = question.help_text,
                                                                      answer_type = question.answer_type,
                                                                      client = client_name,
                                                                      exact_answer = questions,
                                                                      answer = question_choice.answer,
                                                                      created_by  = request.user,
                                                                      modified_by = request.user,
                                                                      )
                            elif question.answer_type == '4':
                                question_slider = CreateQuestionSlider.objects.get(create_question = question)
                                ClientQuestionsAnswers.objects.create(client_question_id = question.id,
                                                                      module = module_assign,
                                                                      question_text =  question.question_text,
                                                                      help_text = question.help_text,
                                                                      answer_type = question.answer_type,
                                                                      client = client_name,
                                                                      exact_answer = questions,
                                                                      min_value = question_slider.min_value,
                                                                      max_value = question_slider.max_value,
                                                                      created_by  = request.user,
                                                                      modified_by = request.user,
                                                                      )
                            else:
                                
                                ClientQuestionsAnswers.objects.create(client_question_id = question.id,
                                                                      module = module_assign,
                                                                      question_text =  question.question_text,
                                                                      help_text = question.help_text,
                                                                      answer_type = question.answer_type,
                                                                      client = client_name,
                                                                      exact_answer = questions,
                                                                      created_by  = request.user,
                                                                      modified_by = request.user,
                                                                      )
                            answer_list.append({'question':question.id, 'answer':questions})
            if answer_list :
                company_treatment = CompanyClientTreatment.objects.get(client__id = client_name.id, id = treat_id, active = True)
                for answer in answer_list:
                    question_id = CreateQuestion.objects.get(id = answer['question'])
                    client_user = Client.objects.get(client_number = request.user.username)
                    ClientQuestions.objects.create(question  = question_id,
                                                   answer    = answer['answer'],
                                                   client_treatment = company_treatment,
                                                   created_by  = request.user,
                                                   modified_by = request.user,
                                                   client      = client_user,
                                                 )
                CompanyClientTreatment.objects.filter(client__id = client_name.id, id = treat_id, active = True).update(question_active_status = False, question_post_status = True, question_post_read_status = True)
                messages.success(request,(_("Questions Saved Successfully")),
                                             fail_silently = True)
                return redirect(reverse('client_questions_list', kwargs={'domain_name': domain_name}))
    except CompanyClientTreatment.DoesNotExist:
        messages.success(request,(_('This Question Module has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_questions_list', kwargs={'domain_name': domain_name}))
    return render_to_response('client/client_question_view.html', locals(), context_instance = RequestContext(request))

@client_login
def client_question_feedback(request, domain_name = None, module_id= None):
    client_name = Client.objects.get(client_number = request.user)
    try:
        select_module = CompanyClientTreatment.objects.get(id = module_id, client__id = client_name.id)
        client_question_answer = ClientQuestionsAnswers.objects.filter(module = select_module, client = client_name)
       
        client_questions = ClientQuestions.objects.filter(client = client_name, question__module__id = select_module.module.id)
        
        client_question_choices = ClientQuestionsAnswers.objects.filter(Q(answer_type = '2')|Q(answer_type = '3'),module = select_module, client = client_name)
        full_choices =[]
        slider_val=[]
        if client_question_choices:
            for client_choice in client_question_choices:
                choice_options = client_choice.answer.splitlines()
                choice_value = []
                for options in choice_options:
                    if not re.match(r'^[\s]*$', options):
                        if not (options == ''):
                            choice_value.append(options)
                full_choices.append({'question':client_choice.client_question_id, 'options':choice_value})
                
        all_slider = ClientQuestionsAnswers.objects.filter(answer_type = '4',module = select_module, client = client_name)
        if all_slider:
            for slider in all_slider:
                slider_val.append({'ques_id':slider.client_question_id,'min_val':slider.min_value, 'max_val':slider.max_value})
                        
        
        exist_feedback = ClientQuestionsFeedback.objects.filter(client = client_name, client_treatment = module_id).order_by('created_at')
        if request.method == "POST":
            form = ClientQuestionsFeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                feedback = form.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientTreatment.objects.filter(client__id = client_name.id, id = module_id, active = True).update(question_active_status = False, question_post_status = True, question_post_read_status = True)
                
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('client_questions_list', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('client/client_question_feedback.html', locals(), context_instance = RequestContext(request))
        form = ClientQuestionsFeedbackForm()
    except CompanyClientTreatment.DoesNotExist:
        messages.success(request,(_('This Question Module has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_questions_list', kwargs={'domain_name': domain_name}))
    return render_to_response('client/client_question_feedback.html', locals(), context_instance = RequestContext(request))