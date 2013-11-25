from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.admin_management.assignments_forms import AssignmentsForm, AssignmentClusterForm, QuestionAnswerForm
from vcg.admin_management.models import  Module, Session, AssignmentQuestion, AssignmentQuestionAnswer, AssignmentCluster, Assignment, AdminUserPermission
from vcg.utilities import Utility, admin_login, permission_view
from vcg.config import choices 

@admin_login
@permission_view('TREAT1', None)
def assignments(request, read_only):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    if request.POST:
        form = AssignmentsForm(request.POST, request.FILES)
        if form.is_valid():
            assign = form.save(commit = False)
            assign.created_by = assign.modified_by = request.user
            assign.save()
            messages.success(request, (_("Assignment Saved Successfully")),
                                         fail_silently = True) 
            return redirect('/admin_management/assignments_cluster/'+str(assign.id)+"/")
        else:
            return render_to_response('admin/assignments.html', locals(), context_instance=RequestContext(request))
    else:
        form = AssignmentsForm()
    return render_to_response('admin/assignments.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT2', 'TREAT3')
def assignments_list(request, read_only):
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    list_of_assignments = Assignment.objects.all()
    key = request.GET.get('keyword')
    if key is not None: 
        key = key.lstrip()
    if key :
        list_of_assignments = Assignment.objects.filter(Q(name__icontains = key))
    else:
        list_of_assignments = Assignment.objects.all()

    paginate  = Paginator(list_of_assignments, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_of_assignments = paginate.page(page)
    except (EmptyPage, InvalidPage):
        list_of_assignments = paginate.page(paginate.num_pages)
    num_pages = range(list_of_assignments.paginator.num_pages)
            
    return render_to_response('admin/assignments_list.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT4')
def assignments_delete(request, read_only):
    if request.method == 'POST':
        assignment_ids    = request.POST.getlist('choices')
        for assignment_id in assignment_ids:
            assignment = Assignment.objects.get(id = assignment_id)
            assignment.delete()
        if len(assignment_ids) > 1:
            messages.success(request,(_("Selected Assignments Deleted Successfully")),fail_silently = True)
        else:    
            messages.success(request,(_("Selected Assignment Deleted Successfully")),fail_silently = True)            
    return redirect('/admin_management/assignments_list/')  

@admin_login
@permission_view('TREAT1', None)
def assignments_cluster(request, read_only, assignment_id = None):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    if request.POST:
        form = AssignmentClusterForm(request.POST, request.FILES, initial={'assignment':assignment_id})
        if form.is_valid():
            assign = form.save(commit = False)
            assign.created_by = assign.modified_by = request.user
            assign.active = True
            assign.save()
            messages.success(request,(_("Assignment Cluster Saved Successfully")),
                                         fail_silently = True) 
            return redirect('/admin_management/assignment_question/'+str(assign.id)+"/0/")
        else:
            return render_to_response('admin/assignments_cluster.html', locals(), context_instance=RequestContext(request))
    else:
        form = AssignmentClusterForm(initial={'assignment':assignment_id})
    return render_to_response('admin/assignments_cluster.html', locals(), context_instance=RequestContext(request))

@admin_login
@permission_view('TREAT1', 'TREAT2')
def assignment_question(request, read_only, cluster_id = None, quest_id = None):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    questions = AssignmentQuestion.objects.filter(assignment_cluster = cluster_id)
    try:
        cluster_names = AssignmentCluster.objects.get(id = cluster_id)
        cluster_name = cluster_names.assignment.id
        
        answerlist=[]
        for quest in questions:
            answers_list = AssignmentQuestionAnswer.objects.filter(assignment_question = quest.id)
            for ans in answers_list:
                answerlist.append(ans)
            
        if request.POST:
            form = QuestionAnswerForm(request.POST, request.FILES)
            if form.is_valid():
                cluster = AssignmentCluster.objects.get(id = cluster_id)
                question = AssignmentQuestion.objects.create(assignment_cluster = cluster,
                                                  question_text = form.cleaned_data['question'],
                                                  active = True)
                assign = AssignmentQuestion.objects.get(id = question.id)
                AssignmentQuestionAnswer.objects.create(assignment_question = question, option = form.cleaned_data['choice_a'],
                                                        answer = form.cleaned_data['answer_a'] , active = True)
                AssignmentQuestionAnswer.objects.create(assignment_question = question, option = form.cleaned_data['choice_b'],
                                                        answer = form.cleaned_data['answer_b'] , active = True)
                AssignmentQuestionAnswer.objects.create(assignment_question = question, option = form.cleaned_data['choice_c'],
                                                        answer = form.cleaned_data['answer_c'] , active = True)
                AssignmentQuestionAnswer.objects.create(assignment_question = question, option = form.cleaned_data['choice_d'],
                                                        answer = form.cleaned_data['answer_d'] , active = True)
                if quest_id == "1":
                    return redirect('/admin_management/assignment_question/'+cluster_id+'/'+quest_id+'/')
                else:
                    return redirect('/admin_management/assignments_list/')
            else:
                return render_to_response('admin/assignment_question.html', locals(), context_instance=RequestContext(request))
        else:
            
            form = QuestionAnswerForm()
        return render_to_response('admin/assignment_question.html', locals(), context_instance=RequestContext(request))
    except AssignmentCluster.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed')), fail_silently= True)
        return redirect('/admin_management/assignments_list/')
    
@admin_login
@permission_view('TREAT2', 'TREAT3')
def assignment_editquestion(request, read_only, cluster_id = None, quest_id = None):
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    
    try:
        try_assignmentquestion = AssignmentQuestion.objects.get(pk = quest_id)
        question = get_object_or_404(AssignmentQuestion, pk = quest_id)
        answers_list_option = AssignmentQuestionAnswer.objects.filter(assignment_question__id = quest_id)
                
        questions = AssignmentQuestion.objects.filter(assignment_cluster = cluster_id)
        answerlist=[]
        for quest in questions:
            answers_list = AssignmentQuestionAnswer.objects.filter(assignment_question = quest.id)
            for ans in answers_list:
                answerlist.append(ans)
        if request.POST:
            form = QuestionAnswerForm(request.POST, request.FILES)
            if form.is_valid():
                cluster = AssignmentCluster.objects.get(id = cluster_id)
                AssignmentQuestion.objects.filter(assignment_cluster = cluster, id = quest_id).update(question_text = form.cleaned_data['question'],
                                                  active = True)
                answers = AssignmentQuestionAnswer.objects.filter(assignment_question__id = quest_id).delete()
                AssignmentQuestionAnswer.objects.create(assignment_question = question, option = form.cleaned_data['choice_a'],
                                                        answer = form.cleaned_data['answer_a'] , active = True)
                AssignmentQuestionAnswer.objects.create(assignment_question = question, option = form.cleaned_data['choice_b'],
                                                        answer = form.cleaned_data['answer_b'] , active = True)
                AssignmentQuestionAnswer.objects.create(assignment_question = question, option = form.cleaned_data['choice_c'],
                                                        answer = form.cleaned_data['answer_c'] , active = True)
                AssignmentQuestionAnswer.objects.create(assignment_question = question, option = form.cleaned_data['choice_d'],
                                                        answer = form.cleaned_data['answer_d'] , active = True)
                messages.success(request,(_("Assignment Edited Successfully")),
                                             fail_silently = True)
                return redirect('/admin_management/assignment_question/'+cluster_id+'/'+quest_id+'/')
                
            else:
                return render_to_response('admin/assignment_editquestion.html', locals(), context_instance=RequestContext(request))
        else:
            
            form = QuestionAnswerForm(initial={'question':question,'choice_a':answers_list_option[0].option,'choice_b':answers_list_option[1].option,'choice_c':answers_list_option[2].option,
                                                                    'choice_d':answers_list_option[3].option, 'answer_a':answers_list_option[0].answer, 'answer_b':answers_list_option[1].answer, 
                                                                    'answer_c':answers_list_option[2].answer, 'answer_d':answers_list_option[3].answer})
        return render_to_response('admin/assignment_editquestion.html', locals(), context_instance=RequestContext(request))
    except AssignmentQuestion.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed')), fail_silently= True)
        return redirect('/admin_management/assignment_list/')
    
@admin_login
@permission_view('TREAT4', None)
def assignment_deletequestion(request, read_only, cluster_id = None, quest_id = None):
    try:
        try_assignment = AssignmentQuestion.objects.get(id = quest_id)
        get_object_or_404(AssignmentQuestion, pk = quest_id).delete()
        AssignmentQuestionAnswer.objects.filter(assignment_question__id = quest_id).delete()
        messages.success(request,(_("Assignment Deleted Successfully")),
                                             fail_silently = True)
        return redirect('/admin_management/assignment_question/'+cluster_id+'/'+quest_id+'/')
    except AssignmentQuestion.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed')), fail_silently= True)
        return redirect('/admin_management/assignment_list/')
    
@admin_login
@permission_view('TREAT2', 'TREAT3')
def edit_assignments(request, read_only, assign_id = None):
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    try:
        try_assignment = Assignment.objects.get(id = assign_id)
        assignment = get_object_or_404(Assignment, pk = assign_id)
        if request.POST:
            form = AssignmentsForm(request.POST, request.FILES, instance = assignment)
            if form.is_valid():
                assign = form.save(commit = False)
                assign.created_by = assign.modified_by = request.user
                assign.save()
                messages.success(request,(_("Assignment Saved Successfully")),
                                             fail_silently = True)
                return redirect('/admin_management/assignments_editcluster/'+str(assign.id)+"/")
            else:
                return render_to_response('admin/assignments.html', locals(), context_instance=RequestContext(request))
        else:
            form = AssignmentsForm(instance = assignment)
        if read_only == "readonly":
            cluster_list = AssignmentCluster.objects.filter(assignment = assignment)
            cluster_questions = AssignmentQuestion.objects.filter(assignment_cluster__assignment__id = assignment.id, active = True).order_by('-created_at')
            answers = AssignmentQuestionAnswer.objects.filter(assignment_question__assignment_cluster__assignment__id = assignment.id)
            return render_to_response('admin/editpermission_assignments.html', locals(), context_instance=RequestContext(request))
        return render_to_response('admin/assignments.html', locals(), context_instance=RequestContext(request))
    except Assignment.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed')), fail_silently= True)
        return redirect('/admin_management/assignment_list/')
    
@admin_login
@permission_view('TREAT2', 'TREAT3')
def assignments_editcluster(request, read_only, assignment_id = None):
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    cluster_list = AssignmentCluster.objects.filter(assignment = assignment_id)
    cluster_questions = AssignmentQuestion.objects.filter(assignment_cluster__assignment__id = assignment_id, active = True).order_by('-created_at')
    quest_list = []
    for clust_quest in cluster_questions:
        quest_list.append(clust_quest)
    return render_to_response('admin/assignments_editcluster.html', locals(), context_instance=RequestContext(request))
    
@admin_login
@permission_view('TREAT4', None)
def assignment_clusterdelete(request, read_only, cluster_id = None):
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    try:
        assign_names = AssignmentCluster.objects.get(id = cluster_id)
        assignment_name = AssignmentCluster.objects.get(id = cluster_id).delete()
        AssignmentQuestion.objects.filter(assignment_cluster__id = cluster_id).delete()
        AssignmentQuestionAnswer.objects.filter(assignment_question__assignment_cluster__id = cluster_id).delete()
        return redirect('/admin_management/assignments_editcluster/'+str(assign_names.assignment.id)+'/')
    except AssignmentCluster.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed')), fail_silently= True)
        return redirect('/admin_management/assignment_list/')
    
@admin_login
@permission_view('TREAT2', 'TREAT3')
def assignment_editclustername(request, read_only, cluster_id = None):
    if not request.user.is_superuser:
        permission = AdminUserPermission.objects.get(admin_user__user_id = request.user).create_file.split(",")
    module_list = Module.objects.filter(active = True)
    session_list = Session.objects.all()
    try:
        try_assignment = AssignmentCluster.objects.get(id = cluster_id)
        cluster_name = get_object_or_404(AssignmentCluster, pk = cluster_id)
        if request.POST:
            form = AssignmentClusterForm(request.POST, request.FILES, instance = cluster_name)
            if form.is_valid():
                assign = form.save(commit = False)
                assign.created_by = assign.modified_by = request.user
                assign.active = True
                assign.save()
                messages.success(request,(_("Assignment Cluster Saved Successfully")),
                                             fail_silently = True)
                return redirect('/admin_management/assignments_editcluster/'+str(cluster_name.assignment.id)+"/")
            else:
                return render_to_response('admin/assignments_cluster.html', locals(), context_instance=RequestContext(request))
        else:
            form = AssignmentClusterForm(instance = cluster_name)
        return render_to_response('admin/assignments_cluster.html', locals(), context_instance=RequestContext(request))
    except AssignmentCluster.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed')), fail_silently= True)
        return redirect('/admin_management/assignment_list/')
    
@admin_login
@permission_view('TREAT4', None)
def delete_assignment(request, read_only, assign_id = None):
    try:
        try_assignment = Assignment.objects.get(id = assign_id)
        Assignment.objects.get(id = assign_id).delete()
        AssignmentCluster.objects.filter(assignment__id = assign_id).delete()
        AssignmentQuestion.objects.filter(assignment_cluster__assignment__id = assign_id).delete()
        AssignmentQuestionAnswer.objects.filter(assignment_question__assignment_cluster__assignment__id = assign_id).delete()
        messages.success(request,(_("Assignment Deleted Successfully")),
                                             fail_silently = True)
        return redirect('/admin_management/assignments_list')
    except Assignment.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed')), fail_silently= True)
        return redirect('/admin_management/assignment_list/')
