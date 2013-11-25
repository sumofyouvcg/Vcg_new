from django.shortcuts import render_to_response,redirect, RequestContext, HttpResponse
from django.utils import simplejson
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Test, TestQuestion, TestRange, TestQuestionAnswers
from vcg.utilities import admin_login, permission_view
from vcg.config import choices

@admin_login
@permission_view('TEST3', None)
def test_list(request, read_only):   
    key = request.GET.get('keyword')

    if key is not None: 
        key = key.lstrip()
    if key :
        tests_list = Test.objects.filter(title__icontains = key, active = True).order_by('-modified_at')
    else:
        tests_list = Test.objects.all().order_by('title').order_by('-modified_at')
    paginate  = Paginator(tests_list, choices.list_per_page)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        test_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        test_list = paginate.page(paginate.num_pages)
    num_pages = range(test_list.paginator.num_pages)
    return render_to_response('admin/test_list.html', locals(), context_instance = RequestContext(request))

@admin_login
@permission_view('TEST2', 'TEST3')
def test_edit(request, read_only, test_id = None):
    try:
        test           = Test.objects.get(id = test_id)
        test_questions = TestQuestion.objects.filter(test__id = test_id).order_by('id')
        test_answers   = TestQuestionAnswers.objects.filter(question__test__id = test.id).order_by('id')
        test_scores    = TestRange.objects.filter(test__id = test_id).order_by('id')

        if request.POST:
    
            title_value = request.POST.get('title').strip()
    
            titles = []
            for each in Test.objects.filter(title = title_value):
                if str(each.id) != str(test_id):
                    titles.append(str(each.title))
            if len(titles) > 0:
                json = simplejson.dumps(_('Test with this title already exists'))
                return HttpResponse(json, mimetype='application/javascript')

            question_ids = []
            for each in request.POST:
                if "question_" in each and "_score_" not in each and "_answer_" not in each:
                    each_question_id = str(each).split('_')[1]
                    question_ids.append(each_question_id)
            question_ids.sort(key = int)

            score_ids = []
            for each in request.POST:
                if "score_from_" in each:
                    score_ids.append(str(each).split('_')[2])
            score_ids.sort(key = int)
    
            json = ''
            if not title_value:
                json = simplejson.dumps(_("Don't leave any fields blank"))
            elif len(title_value) < 4 or len(title_value) > 100:
                json = simplejson.dumps(_("Length of title should be between 4 and 100 characters"))
            else:
                question_no = 0
                for each in question_ids:
                    question_no += 1
                    if not request.POST.get("question_" + str(each)).strip():
                        json = simplejson.dumps(_("Don't leave any fields blank"))
                        break
                    elif len(request.POST.get("question_" + str(each))) < 5 or len(request.POST.get("question_" + str(each))) > 500:
                        json = simplejson.dumps(_("Length of Question %s should be between 5 and 500 characters") % str(question_no))
                        break
                    for each_element in request.POST:
                        if "question_" + str(each) + "_answer_" in each_element:
                            if not request.POST[each_element].strip():
                                json = simplejson.dumps(_("Don't leave any fields blank"))
                                break
                            elif len(request.POST[each_element].strip()) < 1 or len(request.POST[each_element].strip()) > 50:
                                json = simplejson.dumps(_("Length of Answer %(loop1) in Question %(loop2) should be between 1 and 50 characters") % (str(each_element.split('_')[3]), str(each_element.split('_')[1])))
                                break
                        if "question_" + str(each) + "_score_" in each_element:
                            if not request.POST[each_element]:
                                json = simplejson.dumps(_("Don't leave any fields blank"))
                                break
                if not json:
                    score_id = 0
                    for each in score_ids:
                        score_id += 1
                        if not request.POST.get("score_from_" + str(each)) or not request.POST.get("score_to_" + str(each)) or not request.POST.get("score_mean_" + str(each)).strip():
                            json = simplejson.dumps(_("Don't leave any fields blank"))
                            break
                        elif len(request.POST.get("score_mean_" + str(each))) < 2 or len(request.POST.get("score_mean_" + str(each))) > 250:
                            json = simplejson.dumps(_("Length of score result %s should be between 2 and 250 characters") % str(score_id))
                            break
                if not json:
                    loop_id = 0
                    for each_id in score_ids:
                        if int(each_id) == 1:
                            if int(request.POST.get("score_from_" + str(each_id))) >= int(request.POST.get("score_to_" + str(each_id))):
                                json = simplejson.dumps(_("Check score values in row 1"))
                                break
                        else:
                            if int(request.POST.get("score_to_" + str(score_ids[loop_id - 1]))) != (int(request.POST.get("score_from_" + str(score_ids[loop_id]))) - 1):
                                json = simplejson.dumps(_("Check end value in row %(loop1) and start value in row %(loop2)") % (str(loop_id), str(loop_id + 1)))
                                break
                            elif int(request.POST.get("score_from_" + str(score_ids[loop_id]))) >= int(request.POST.get("score_to_" + str(score_ids[loop_id]))):
                                json = simplejson.dumps(_("Check score values in row %s") % str(loop_id + 1))
                                break
                        loop_id += 1
            if json:
                return HttpResponse(json, mimetype='application/javascript')

            #To update test title
            active = True
            if not request.POST.get('active'):
                active = False
            Test.objects.filter(id = test_id).update(title       = title_value.strip(),
                                                     active      = active,
                                                     created_by  = request.user,
                                                     modified_by = request.user
                                                     )
            test = Test.objects.get(title = title_value)

            #To update test questions and answers
            test_questions.delete()
            for id_number in question_ids:
                question = TestQuestion.objects.create(test        = test,
                                                       question    = request.POST.get("question_" + str(id_number)).strip(),
                                                       created_by  = request.user,
                                                       modified_by = request.user
                                                       )
                answer_ids = []
                for each_element in request.POST:
                    if "question_" + str(id_number) + "_answer_" in each_element:
                        answer_ids.append(str(each_element).split('_')[3])
                answer_ids.sort(key = int)
                for each_answer_id in answer_ids:
                    TestQuestionAnswers.objects.create(question = question,
                                                       answer   = request.POST["question_" + str(id_number) + "_answer_" + str(each_answer_id)],
                                                       score    = request.POST["question_" + str(id_number) + "_score_" + str(each_answer_id)],
                                                       )

            #To update test scores
            test_scores.delete()
            for id_number in score_ids:
                TestRange.objects.create(test        = test,
                                         from_value  = request.POST.get("score_from_" + str(id_number)),
                                         to_value    = request.POST.get("score_to_" + str(id_number)),
                                         result      = request.POST.get("score_mean_" + str(id_number)).strip(),
                                         created_by  = request.user,
                                         modified_by = request.user
                                         )

            messages.success(request, (_("Test Saved Successfully")), fail_silently = True)
            json = simplejson.dumps('save_success')
            return HttpResponse(json, mimetype='application/javascript')
        return render_to_response('admin/test_edit.html', locals(), context_instance = RequestContext(request))
    except Test.DoesNotExist:
        messages.success(request,(_('This Test has been removed')), fail_silently= True)
        return redirect('/admin_management/test_list/')
    
@admin_login
@permission_view('TEST1', None)
def test_add(request, read_only):

    if request.POST:
        title_value = request.POST.get('title').strip()

        if Test.objects.filter(title = title_value):
            json = simplejson.dumps(_('Test with this title already exists'))
            return HttpResponse(json, mimetype='application/javascript')

        question_ids = []
        for each in request.POST:
            if "question_" in each and "_score_" not in each and "_answer_" not in each:
                each_question_id = str(each).split('_')[1]
                question_ids.append(each_question_id)
        question_ids.sort(key = int)

        score_ids = []
        for each in request.POST:
            if "score_from_" in each:
                score_ids.append(str(each).split('_')[2])
        score_ids.sort(key = int)

        json = ''
        if not title_value:
            json = simplejson.dumps(_("Don't leave any fields blank"))
        elif len(title_value) < 1 or len(title_value) > 100:
            json = simplejson.dumps(_("Length of title should be between 1 and 100 characters"))
        else:
            question_no = 0
            for each in question_ids:
                question_no += 1
                if not request.POST.get("question_" + str(each)).strip():
                    json = simplejson.dumps(_("Don't leave any fields blank"))
                    break
                elif len(request.POST.get("question_" + str(each))) < 1 or len(request.POST.get("question_" + str(each))) > 500:
                    json = simplejson.dumps(_("Length of Question %s should be between 1 and 500 characters") % str(question_no))
                    break
                for each_element in request.POST:
                    if "question_" + str(each) + "_answer_" in each_element:
                        if not request.POST[each_element].strip():
                            json = simplejson.dumps(_("Don't leave any fields blank"))
                            break
                        elif len(request.POST[each_element].strip()) < 1 or len(request.POST[each_element].strip()) > 50:
                            json = simplejson.dumps(_("Length of Answer %(loop1) in Question %(loop2) should be between 1 and 50 characters") % (str(each_element.split('_')[3]), str(each_element.split('_')[1])))
                            break
                    if "question_" + str(each) + "_score_" in each_element:
                        if not request.POST[each_element]:
                            json = simplejson.dumps(_("Don't leave any fields blank"))
                            break
            if not json:
                score_id = 0
                for each in score_ids:
                    score_id += 1
                    if not request.POST.get("score_from_" + str(each)) or not request.POST.get("score_to_" + str(each)) or not request.POST.get("score_mean_" + str(each)).strip():
                        json = simplejson.dumps(_("Don't leave any fields blank"))
                        break
                    elif len(request.POST.get("score_mean_" + str(each))) < 1 or len(request.POST.get("score_mean_" + str(each))) > 250:
                        json = simplejson.dumps(_("Length of score result %s should be between 1 and 250 characters") % str(score_id))
                        break
            if not json:
                loop_id = 0
                for each_id in score_ids:
                    if int(each_id) == 1:
                        if int(request.POST.get("score_from_" + str(each_id))) >= int(request.POST.get("score_to_" + str(each_id))):
                            json = simplejson.dumps(_("Check score values in row 1"))
                            break
                    else:
                        if int(request.POST.get("score_to_" + str(score_ids[loop_id - 1]))) != (int(request.POST.get("score_from_" + str(score_ids[loop_id]))) - 1):
                            json = simplejson.dumps(_("Check end value in row %(loop1) and start value in row %(loop2)") % (str(loop_id), str(loop_id + 1)))
                            break
                        elif int(request.POST.get("score_from_" + str(score_ids[loop_id]))) >= int(request.POST.get("score_to_" + str(score_ids[loop_id]))):
                            json = simplejson.dumps(_("Check score values in row %s") % str(loop_id + 1))
                            break
                    loop_id += 1
        if json:
            return HttpResponse(json, mimetype='application/javascript')

        #To add test title
        active = True
        if not request.POST.get('active'):
            active = False
        test = Test.objects.create(title       = title_value,
                                   active      = active,
                                   created_by  = request.user,
                                   modified_by = request.user
                                   )

        #To add test questions and answers
        for id_number in question_ids:
            question = TestQuestion.objects.create(test        = test,
                                                   question    = request.POST.get("question_" + str(id_number)).strip(),
                                                   created_by  = request.user,
                                                   modified_by = request.user
                                                   )
            answer_ids = []
            for each_element in request.POST:
                if "question_" + str(id_number) + "_answer_" in each_element:
                    answer_ids.append(str(each_element).split('_')[3])
            answer_ids.sort(key = int)
            for each_answer_id in answer_ids:
                TestQuestionAnswers.objects.create(question = question,
                                                   answer   = request.POST["question_" + str(id_number) + "_answer_" + str(each_answer_id)],
                                                   score    = request.POST["question_" + str(id_number) + "_score_" + str(each_answer_id)],
                                                   )

        #To add test scores
        for id_number in score_ids:
            TestRange.objects.create(test        = test,
                                     from_value  = request.POST.get("score_from_" + str(id_number)),
                                     to_value    = request.POST.get("score_to_" + str(id_number)),
                                     result      = request.POST.get("score_mean_" + str(id_number)).strip(),
                                     created_by  = request.user,
                                     modified_by = request.user
                                     )

        messages.success(request,(_("Test Saved Successfully")), fail_silently = True)
        json = simplejson.dumps('save_success')
        return HttpResponse(json, mimetype='application/javascript')
    return render_to_response('admin/test_add.html', locals(), context_instance = RequestContext(request))

@admin_login
@permission_view('TEST4')
def test_delete(request, read_only):
    if request.method == 'POST':
        test_ids    = request.POST.getlist('choices')
        for test_id in test_ids:
            test = Test.objects.get(id = test_id)
            test.delete()
        if len(test_ids) > 1:
            messages.success(request,(_("Selected Tests Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Test Deleted Successfully")),fail_silently = True)            
    return redirect('/admin_management/test_list/')
