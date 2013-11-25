import re

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.diary_forms import DiaryForm, DiaryQuestionForm, QuestionChoiceForm, QuestionSliderForm
from vcg.admin_management.models import Diary, DiaryQuestion, QuestionChoice, QuestionSlider
from vcg.utilities import Utility, admin_login, permission_view
from vcg.config import choices

@admin_login
@permission_view('DIA3', None)
def diary_list(request, read_only):   
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        diary_list = Diary.objects.filter(Q(title__icontains = key)|Q(diary_number__icontains = key)).order_by('-modified_at')
    else:
        diary_list = Diary.objects.filter().order_by('-modified_at')
    ques_count = []
    if diary_list:
        for diary in diary_list:
            questions = DiaryQuestion.objects.filter(diary__id = diary.id)
            ques_count.append({'diary_id':diary.id,'no_of_ques':len(questions)})

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
                
    return render_to_response('admin/diary_list.html', locals(), context_instance = RequestContext(request))

@admin_login
@permission_view('DIA1', None)
def diary_add(request, read_only):
    if request.method == "POST":
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary = form.save(commit = False)
            diary.created_by = diary.modified_by = request.user
            diary.save()
            diary_id = diary.id
            return redirect('/admin_management/diary_question/'+str(diary_id)+"/1/")
        else:
            return render_to_response('admin/diary_add.html', locals(), context_instance = RequestContext(request))    
    else:
        form = DiaryForm()
    return render_to_response('admin/diary_add.html', locals(), context_instance = RequestContext(request))

@admin_login
@permission_view('DIA2', 'DIA3')
def diary_question(request, read_only, diary_id = None, add_ques = None):
    try:
        try_diary = Diary.objects.get(id = diary_id)
        if request.method == "POST":
            form = DiaryQuestionForm(request.POST, request.FILES)
            form1 = QuestionChoiceForm(request.POST, request.FILES)
            form2 = QuestionSliderForm(request.POST, request.FILES)
            if form.is_valid():
                question = form.save(commit = False)
                question.diary_id = diary_id
                question.created_by = question.modified_by = request.user
                question.active = True
                if question.answer_type == '2' or question.answer_type == '3':
                    if form1.is_valid():
                        question.save()
                        ques_id = question.id
                        choice = form1.save(commit = False)
                        choice.diary_question_id = question.id
                        choice.created_by = choice.modified_by = request.user
                        choice.save()
                    else:
                        ans_type="text"
                        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
                        return render_to_response('admin/diary_question.html', locals(), context_instance = RequestContext(request))  
                elif question.answer_type == '4':
                    if form2.is_valid():
                        question.save()
                        ques_id = question.id
                        slider = form2.save(commit = False)
                        slider.diary_question_id = question.id
                        slider.created_by = slider.modified_by = request.user
                        slider.save()
                    else:
                        ans_type="slider"
                        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
                        return render_to_response('admin/diary_question.html', locals(), context_instance = RequestContext(request))    
                else:
                    question.save()
                    ques_id = question.id
                
                if add_ques == '1':
                    return redirect('/admin_management/diary_question/'+str(diary_id)+'/'+str(add_ques)+'/')
                else:
                    messages.success(request,(_("Diary Saved Successfully")), fail_silently = True)
                    return redirect('/admin_management/diary_list/')
            else:
                return render_to_response('admin/diary_question.html', locals(), context_instance = RequestContext(request))    
        else:
            form = DiaryQuestionForm()
            form1 = QuestionChoiceForm()
            form2 = QuestionSliderForm()
        slider_val=[]
        choice_val=[]
        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
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
        diary_detail = Diary.objects.get(id = diary_id)
        
        return render_to_response('admin/diary_question.html', locals(), context_instance = RequestContext(request))
    except Diary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed')), fail_silently= True)
        return redirect('/admin_management/diary_list/')
    
@admin_login
@permission_view('DIA2', 'DIA3')
def edit_diary_question(request, read_only, diary_id = None, ques_id = None):
    try:
        try_diary = Diary.objects.get(id = diary_id)
        if request.method == "POST":
            del_choice = QuestionChoice.objects.filter(diary_question__id = ques_id)
            if del_choice:
                del_choice.delete()
            del_slider = QuestionSlider.objects.filter(diary_question__id = ques_id)
            if del_slider:
                del_slider.delete()
            del_ques = DiaryQuestion.objects.filter(id = ques_id)
            if del_ques:
                del_ques.delete()
            form = DiaryQuestionForm(request.POST, request.FILES)
            form1 = QuestionChoiceForm(request.POST, request.FILES)
            form2 = QuestionSliderForm(request.POST, request.FILES)
            if form.is_valid():
                question = form.save(commit = False)
                question.diary_id = diary_id
                question.created_by = question.modified_by = request.user
                question.active = True
                if question.answer_type == '2' or question.answer_type == '3':
                    if form1.is_valid():
                        question.save()
                        ques_id = question.id
                        choice = form1.save(commit = False)
                        choice.diary_question_id = question.id
                        choice.created_by = choice.modified_by = request.user
                        choice.save()
                    else:
                        ans_type="text"
                        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
                        return render_to_response('admin/edit_diary_question.html', locals(), context_instance = RequestContext(request))  
                elif question.answer_type == '4':
                    if form2.is_valid():
                        question.save()
                        ques_id = question.id
                        slider = form2.save(commit = False)
                        slider.diary_question_id = question.id
                        slider.created_by = slider.modified_by = request.user
                        slider.save()
                    else:
                        ans_type="slider"
                        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
                        return render_to_response('admin/edit_diary_question.html', locals(), context_instance = RequestContext(request))    
                else:
                    question.save()
                    ques_id = question.id    
                return redirect('/admin_management/diary_question/'+str(diary_id)+'/0/')    
            else:
                return render_to_response('admin/edit_diary_question.html', locals(), context_instance = RequestContext(request))
                
        else:
            edit_ques = DiaryQuestion.objects.filter(id = ques_id)
            edit_choice = QuestionChoice.objects.filter(diary_question__id = ques_id)
            edit_slider = QuestionSlider.objects.filter(diary_question__id = ques_id)
            form = DiaryQuestionForm(instance = edit_ques[0])
            if edit_choice:
                form1 = QuestionChoiceForm(instance = edit_choice[0])
            else:
                form1 = QuestionChoiceForm()
            if edit_slider:
                form2 = QuestionSliderForm(instance = edit_slider[0])
            else:
                form2 = QuestionSliderForm()    
                
            return render_to_response('admin/edit_diary_question.html', locals(), context_instance = RequestContext(request))
    except Diary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed')), fail_silently= True)
        return redirect('/admin_management/diary_list/')

@admin_login
@permission_view('DIA2', 'DIA3')
def delete_diary_question(request, read_only, diary_id = None, ques_id = None):
    try:
        try_diary = Diary.objects.get(id = diary_id)
        del_choice = QuestionChoice.objects.filter(diary_question__id = ques_id)
        if del_choice:
            del_choice.delete()
        del_slider = QuestionSlider.objects.filter(diary_question__id = ques_id)
        if del_slider:
            del_slider.delete()
        del_ques = DiaryQuestion.objects.filter(id = ques_id)
        if del_ques:
            del_ques.delete()
        
        del_diary = DiaryQuestion.objects.filter(diary__id = diary_id)
        if not del_diary:
            diary = Diary.objects.filter(id = diary_id)
            if diary:
                diary.delete()
            return redirect('/admin_management/diary_list/')
                
        return redirect('/admin_management/diary_question/'+str(diary_id)+'/0/')
    except Diary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed')), fail_silently= True)
        return redirect('/admin_management/diary_list/')

@admin_login
@permission_view('DIA2', 'DIA3')
def diary_edit(request, read_only, diary_id = None):   
    try:
        diary_detail = Diary.objects.get(id = diary_id)
        selected_diary = get_object_or_404(Diary, pk = diary_id)
        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
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
    #    if all_ques:
    #        all_choice = QuestionChoice.objects.filter(diary_question__id = all_ques[0].id)
    #        all_slider = QuestionSlider.objects.filter(diary_question__id = all_ques[0].id)
        if request.method == "POST":
            form = DiaryForm(request.POST, request.FILES, instance = selected_diary)
            if form.is_valid():
                diary = form.save(commit = False)
                diary.created_by = diary.modified_by = request.user
                diary.save()
                messages.success(request,(_("Diary Edited Successfully")),fail_silently = True)
                return redirect('/admin_management/diary_list/')
            else:
                return render_to_response('admin/diary_edit.html', locals(), context_instance = RequestContext(request))    
        else:
            form = DiaryForm(instance = selected_diary)
        return render_to_response('admin/diary_edit.html', locals(), context_instance = RequestContext(request))
    except Diary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed')), fail_silently= True)
        return redirect('/admin_management/diary_list/')


@admin_login
@permission_view('DIA2', 'DIA3')
def diary_question1(request, read_only, diary_id = None):
    try:
        try_diary = Diary.objects.get(id = diary_id)
        if request.method == "POST":
            form = DiaryQuestionForm(request.POST, request.FILES)
            form1 = QuestionChoiceForm(request.POST, request.FILES)
            form2 = QuestionSliderForm(request.POST, request.FILES)
            if form.is_valid():
                question = form.save(commit = False)
                question.diary_id = diary_id
                question.created_by = question.modified_by = request.user
                question.active = True
                if question.answer_type == '2' or question.answer_type == '3':
                    if form1.is_valid():
                        question.save()
                        ques_id = question.id
                        choice = form1.save(commit = False)
                        choice.diary_question_id = question.id
                        choice.created_by = choice.modified_by = request.user
                        choice.save()
                    else:
                        ans_type="text"
                        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
                        return render_to_response('admin/diary_question1.html', locals(), context_instance = RequestContext(request))  
                elif question.answer_type == '4':
                    if form2.is_valid():
                        question.save()
                        ques_id = question.id
                        slider = form2.save(commit = False)
                        slider.diary_question_id = question.id
                        slider.created_by = slider.modified_by = request.user
                        slider.save()
                    else:
                        ans_type="slider"
                        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
                        return render_to_response('admin/diary_question1.html', locals(), context_instance = RequestContext(request))    
                else:
                    question.save()
                    ques_id = question.id    
                messages.success(request,(_("Diary Saved Successfully")),fail_silently = True)
                return redirect('/admin_management/diary_edit/'+str(diary_id)+'/')
            else:
                return render_to_response('admin/diary_question1.html', locals(), context_instance = RequestContext(request))    
        else:
            form = DiaryQuestionForm()
            form1 = QuestionChoiceForm()
            form2 = QuestionSliderForm()
        return render_to_response('admin/diary_question1.html', locals(), context_instance = RequestContext(request))
    except Diary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed')), fail_silently= True)
        return redirect('/admin_management/diary_list/')

@admin_login
@permission_view('DIA2', 'DIA3')
def diary_question_edit(request, read_only, diary_id = None, ques_id = None):
    try:
        try_diary = Diary.objects.get(id = diary_id)
        if request.method == "POST":
            del_choice = QuestionChoice.objects.filter(diary_question__id = ques_id)
            if del_choice:
                del_choice.delete()
            del_slider = QuestionSlider.objects.filter(diary_question__id = ques_id)
            if del_slider:
                del_slider.delete()
            del_ques = DiaryQuestion.objects.filter(id = ques_id)
            if del_ques:
                del_ques.delete()
            form = DiaryQuestionForm(request.POST, request.FILES)
            form1 = QuestionChoiceForm(request.POST, request.FILES)
            form2 = QuestionSliderForm(request.POST, request.FILES)
            if form.is_valid():
                question = form.save(commit = False)
                question.id = ques_id
                question.diary_id = diary_id
                question.created_by = question.modified_by = request.user
                question.active = True
                if question.answer_type == '2' or question.answer_type == '3':
                    if form1.is_valid():
                        question.save()
                        ques_id = question.id
                        choice = form1.save(commit = False)
                        choice.diary_question_id = question.id
                        choice.created_by = choice.modified_by = request.user
                        choice.save()
                    else:
                        ans_type="text"
                        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
                        return render_to_response('admin/diary_question_edit.html', locals(), context_instance = RequestContext(request))  
                elif question.answer_type == '4':
                    if form2.is_valid():
                        question.save()
                        ques_id = question.id
                        slider = form2.save(commit = False)
                        slider.diary_question_id = question.id
                        slider.created_by = slider.modified_by = request.user
                        slider.save()
                    else:
                        ans_type="slider"
                        all_ques = DiaryQuestion.objects.filter(diary__id = diary_id)
                        return render_to_response('admin/diary_question_edit.html', locals(), context_instance = RequestContext(request))    
                else:
                    question.save()
                    ques_id = question.id    
                return redirect('/admin_management/diary_edit/'+str(diary_id)+'/')    
            else:
                return render_to_response('admin/diary_question_edit.html', locals(), context_instance = RequestContext(request))
                
        else:
            edit_ques = DiaryQuestion.objects.filter(id = ques_id)
            edit_choice = QuestionChoice.objects.filter(diary_question__id = ques_id)
            edit_slider = QuestionSlider.objects.filter(diary_question__id = ques_id)
            form = DiaryQuestionForm(instance = edit_ques[0])
            if edit_choice:
                form1 = QuestionChoiceForm(instance = edit_choice[0])
            else:
                form1 = QuestionChoiceForm()    
            if edit_slider:
                form2 = QuestionSliderForm(instance = edit_slider[0])
            else:
                form2 = QuestionSliderForm()    
                
            return render_to_response('admin/diary_question_edit.html', locals(), context_instance = RequestContext(request))
    except Diary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed')), fail_silently= True)
        return redirect('/admin_management/diary_list/')

@admin_login
@permission_view('DIA2', 'DIA3')
def diary_question_delete(request, read_only, diary_id = None, ques_id = None):
    try:
        try_diary = Diary.objects.get(id = diary_id)
        del_choice = QuestionChoice.objects.filter(diary_question__id = ques_id)
        if del_choice:
            del_choice.delete()
        del_slider = QuestionSlider.objects.filter(diary_question__id = ques_id)
        if del_slider:
            del_slider.delete()
        del_ques = DiaryQuestion.objects.filter(id = ques_id)
        if del_ques:
            del_ques.delete()
        
        del_diary = DiaryQuestion.objects.filter(diary__id = diary_id)
        if not del_diary:
            diary = Diary.objects.filter(id = diary_id)
            if diary:
                diary.delete()
            return redirect('/admin_management/diary_list/')
                
        return redirect('/admin_management/diary_edit/'+str(diary_id)+'/')
    except Diary.DoesNotExist:
        messages.success(request,(_('This Diary has been removed')), fail_silently= True)
        return redirect('/admin_management/diary_list/')
    
@admin_login
@permission_view('DIA4')
def diary_delete(request, read_only):
    if request.method == 'POST':
        diary_ids    = request.POST.getlist('choices')
        for diary_id in diary_ids:
            diary = Diary.objects.get(id = diary_id)
            diary.delete()
        if len(diary_ids) > 1:
            messages.success(request,(_("Selected Diaries Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Diary Deleted Successfully")),fail_silently = True)            
    return redirect('/admin_management/diary_list/')
