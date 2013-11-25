import re

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.questions_forms import CreateQuestionForm, CreateQuestionChoiceForm, CreateQuestionSliderForm
from vcg.admin_management.models import Module, Session, CreateQuestion, CreateQuestionChoice, CreateQuestionSlider, AdminUserPermission
from vcg.utilities import admin_login, permission_view
from vcg.config import choices

@admin_login
@permission_view('TREAT2', 'TREAT3')
def questions_list(request, read_only):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")

    module_lists = CreateQuestion.objects.filter(active = True).values_list('module').distinct()
    module_question_lists = Module.objects.filter(Q(id__in = module_lists), active = True)

    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        search = key
        module_question_lists = Module.objects.filter(Q(name__icontains = key), active = True)

    question_list = []
    for module in module_question_lists:
        question = CreateQuestion.objects.filter(module = module, active = True).order_by('created_at')
        if question:
            question = CreateQuestion.objects.filter(module = module, active = True).order_by('created_at')[0]
            question_list.append({"id":question.module.id, "module":question.module,"created_at":question.created_at, "modified_at":question.modified_at})

    paginate  = Paginator(question_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        question_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        question_list = paginate.page(paginate.num_pages)
    num_pages = range(question_list.paginator.num_pages)
            
    return render_to_response('admin/questions_list.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT1', None)
def create_questions(request, read_only, module = None):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    if request.POST:
        form = CreateQuestionForm(request.POST, request.FILES)
        form1 = CreateQuestionChoiceForm(request.POST, request.FILES)
        form2 = CreateQuestionSliderForm(request.POST, request.FILES)
        
        if form.is_valid():
            question = form.save(commit = False)
            question.created_by = question.modified_by = request.user
            question.active = True
            if question.answer_type == '2' or question.answer_type == '3':
                if form1.is_valid():
                    question.save()
                    ques_id = question.id
                    choice = form1.save(commit = False)
                    choice.create_question_id = question.id
                    choice.created_by = choice.modified_by = request.user
                    choice.save()
                else:
                    ans_type="text"
                    all_ques = CreateQuestion.objects.filter(id = question.id)
                    return render_to_response('admin/create_questions.html', locals(), context_instance = RequestContext(request))  
            elif question.answer_type == '4':
                if form2.is_valid():
                    question.save()
                    ques_id = question.id
                    slider = form2.save(commit = False)
                    slider.create_question_id = question.id
                    slider.created_by = slider.modified_by = request.user
                    slider.save()
                else:
                    ans_type="slider"
                    all_ques = CreateQuestion.objects.filter(id = question.id)
                    return render_to_response('admin/create_questions.html', locals(), context_instance = RequestContext(request))
            else:
                question.save()
                ques_id = question.id       
            messages.success(request,(_("Questions Saved Successfully")),fail_silently = True)
            return redirect('/admin_management/questions_list/')
        else:
            return render_to_response('admin/create_questions.html', locals(), context_instance=RequestContext(request))
    else:
        form = CreateQuestionForm()
        form1 = CreateQuestionChoiceForm()
        form2 = CreateQuestionSliderForm()
    
    return render_to_response('admin/create_questions.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT1', 'TREAT2')
def add_module_questions(request, read_only, module_id = None):
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    try:
        diary_detail = Module.objects.get(id = module_id)
        module_list = Module.objects.filter(active = True)
        session_list = Session.objects.all()
        if request.POST:
            form = CreateQuestionForm(request.POST, request.FILES)
            form1 = CreateQuestionChoiceForm(request.POST, request.FILES)
            form2 = CreateQuestionSliderForm(request.POST, request.FILES)
            if form.is_valid():
                question = form.save(commit = False)
                question.created_by = question.modified_by = request.user
                question.active = True
                if question.answer_type == '2' or question.answer_type == '3':
                    if form1.is_valid():
                        question.save()
                        ques_id = question.id
                        choice = form1.save(commit = False)
                        choice.create_question_id = question.id
                        choice.created_by = choice.modified_by = request.user
                        choice.save()
                    else:
                        ans_type="text"
                        all_ques = CreateQuestion.objects.filter(id = question.id)
                        return render_to_response('admin/create_questions.html', locals(), context_instance = RequestContext(request))  
                elif question.answer_type == '4':
                    if form2.is_valid():
                        question.save()
                        ques_id = question.id
                        slider = form2.save(commit = False)
                        slider.create_question_id = question.id
                        slider.created_by = slider.modified_by = request.user
                        slider.save()
                    else:
                        ans_type="slider"
                        all_ques = CreateQuestion.objects.filter(id = question.id)
                        return render_to_response('admin/create_questions.html', locals(), context_instance = RequestContext(request))
                else:
                    question.save()
                    ques_id = question.id    
                messages.success(request,(_("Questions Saved Successfully")),fail_silently = True)
                return redirect('/admin_management/add_module_questions/'+str(question.module_id)+'/')
            else:
                return render_to_response('admin/create_questions.html', locals(), context_instance=RequestContext(request))
        else:
            form = CreateQuestionForm(initial={'module':module_id})
            form1 = CreateQuestionChoiceForm()
            form2 = CreateQuestionSliderForm()
        slider_val=[]
        choice_val=[]
        all_ques = CreateQuestion.objects.filter(module__id = module_id)
        if all_ques:
            for ques in all_ques:
                all_choice = CreateQuestionChoice.objects.filter(create_question__module__id = ques.id)
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
        diary_detail = Module.objects.get(id = module_id)
        return render_to_response('admin/create_questions.html', locals(), context_instance=RequestContext(request))
    except Module.DoesNotExist:
        messages.success(request,(_('This Question Module has been removed')), fail_silently= True)
        return redirect('/admin_management/questions_list/')
    
@admin_login
@permission_view('TREAT2', 'TREAT3')
def edit_createquestion(request, read_only, module_id = None, question_id = None):
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    print "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",question_id
    try:
        try_question = Module.objects.get(id = module_id)
        if request.method == "POST":
            del_choice = CreateQuestionChoice.objects.filter(create_question__id = question_id)
            if del_choice:
                del_choice.delete()
            del_slider = CreateQuestionSlider.objects.filter(create_question__id = question_id)
            if del_slider:
                del_slider.delete()
            del_ques = CreateQuestion.objects.filter(id = question_id)
            if del_ques:
                del_ques.delete()
            form = CreateQuestionForm(request.POST, request.FILES)
            form1 = CreateQuestionChoiceForm(request.POST, request.FILES)
            form2 = CreateQuestionSliderForm(request.POST, request.FILES)
            if form.is_valid():
                question = form.save(commit = False)
                question.id = question_id
                question.module_id = module_id
                question.created_by = question.modified_by = request.user
                question.active = True
                
                if question.answer_type == '2' or question.answer_type == '3':
                    if form1.is_valid():
                        question.save()
                        ques_id = question.id
                        choice = form1.save(commit = False)
                        choice.create_question_id = question.id
                        choice.created_by = choice.modified_by = request.user
                        choice.save()
                    else:
                        ans_type="text"
                        all_ques = CreateQuestion.objects.filter(module__id = module_id)
                        return render_to_response('admin/edit_createquestion.html', locals(), context_instance = RequestContext(request))  
                elif question.answer_type == '4':
                    if form2.is_valid():
                        question.save()
                        ques_id = question.id
                        slider = form2.save(commit = False)
                        slider.create_question_id = question.id
                        slider.created_by = slider.modified_by = request.user
                        slider.save()
                    else:
                        ans_type="slider"
                        all_ques = CreateQuestion.objects.filter(module__id = module_id)
                        return render_to_response('admin/edit_createquestion.html', locals(), context_instance = RequestContext(request))    
                else:
                    question.save()
                    ques_id = question.id
                messages.success(request,(_("Question Saved Successfully")),fail_silently = True)
                return redirect('/admin_management/questions_edit/'+str(module_id)+'/')    
            else:
                return render_to_response('admin/edit_createquestion.html', locals(), context_instance = RequestContext(request))
                
        else:
            edit_ques = CreateQuestion.objects.filter(id = question_id)
            print "edit_quesedit_quesedit_quesedit_quesedit_ques", edit_ques
            edit_choice = CreateQuestionChoice.objects.filter(create_question__id = question_id)
            edit_slider = CreateQuestionSlider.objects.filter(create_question__id = question_id)
            form = CreateQuestionForm(instance = edit_ques[0])
            if edit_choice:
                form1 = CreateQuestionChoiceForm(instance = edit_choice[0])
            else:
                form1 = CreateQuestionChoiceForm()    
            if edit_slider:
                form2 = CreateQuestionSliderForm(instance = edit_slider[0])
            else:
                form2 = CreateQuestionSliderForm()    
            module = Module.objects.get(id = module_id)   
            
            return render_to_response('admin/edit_createquestion.html', locals(), context_instance = RequestContext(request))
    except Module.DoesNotExist:
        messages.success(request,(_('This Question Module has been removed')), fail_silently= True)
        return redirect('/admin_management/questions_list/')
    
@admin_login
@permission_view('TREAT4', None)
def question_delete(request, read_only, module_id = None, ques_id = None):
    try:
        try_module = Module.objects.get(id = module_id)
        del_choice = CreateQuestion.objects.filter(id = ques_id)
        if del_choice:
            del_choice.delete()
        del_slider = CreateQuestionSlider.objects.filter(create_question__id = ques_id)
        if del_slider:
            del_slider.delete()
        del_ques = CreateQuestion.objects.filter(id = ques_id)
        if del_ques:
            del_ques.delete()
        
        del_diary = CreateQuestion.objects.filter(module__id = module_id)
        if not del_diary:
            quest = CreateQuestion.objects.filter(id = module_id)
            if quest:
                quest.delete()
            return redirect('/admin_management/questions_list/')
        
        return redirect('/admin_management/questions_edit/'+str(module_id)+'/')
    except Module.DoesNotExist:
        messages.success(request,(_('This Question Module has been removed')), fail_silently= True)
        return redirect('/admin_management/questions_list/')
    
@admin_login
@permission_view('TREAT2', 'TREAT3')
def questions_edit(request, read_only, module_id = None):  
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    try:
        diary_detail = Module.objects.get(id = module_id)
        selected_diary = get_object_or_404(Module, pk = module_id)
        all_ques = CreateQuestion.objects.filter(module__id = module_id)
        slider_val=[]
        choice_val=[]
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
    #    if all_ques:
    #        all_choice = QuestionChoice.objects.filter(diary_question__id = all_ques[0].id)
    #        all_slider = QuestionSlider.objects.filter(diary_question__id = all_ques[0].id)
        if request.method == "POST":
            form = CreateQuestionForm(request.POST, request.FILES, instance = selected_diary)
            if form.is_valid():
                diary = form.save(commit = False)
                diary.created_by = diary.modified_by = request.user
                diary.active = True
                diary.save()
                messages.success(request,(_("Question Edited Successfully")),fail_silently = True)
                return redirect('/admin_management/question_list/')
            else:
                return render_to_response('admin/question_edit.html', locals(), context_instance = RequestContext(request))    
        else:
            form = CreateQuestionForm(instance = selected_diary)
        return render_to_response('admin/question_edit.html', locals(), context_instance = RequestContext(request))
    except Module.DoesNotExist:
        messages.success(request,(_('This Question Module has been removed')), fail_silently= True)
        return redirect('/admin_management/questions_list/')
