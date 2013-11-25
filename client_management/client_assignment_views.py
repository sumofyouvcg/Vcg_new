from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vcg.admin_management.models import AssignmentCluster, AssignmentQuestion, AssignmentQuestionAnswer
from vcg.company_management.models import CompanyClientAssignment
from vcg.client_management.models import ClientAssignment, AssignmentFeedback
from vcg.client_management.client_assignment_forms import AssignmentFeedbackForm
from vcg.utilities import client_login
from vcg.config import choices

@client_login
def client_assignment_list(request, domain_name = None):  
    assignment_list =  CompanyClientAssignment.objects.filter(client__client_number = request.user.username, active = True)

    paginate  = Paginator(assignment_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        assignment_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        assignment_list = paginate.page(paginate.num_pages)
    num_pages = range(assignment_list.paginator.num_pages)
    return render_to_response('client/client_assignment_list.html', locals(), context_instance = RequestContext(request))

@client_login
def client_assignment_questions(request, domain_name = None, assign_id = None):
    CompanyClientAssignment.objects.filter(id = assign_id).update(assign_status = False)
    
    try:
        asssignment = CompanyClientAssignment.objects.get(pk = assign_id)
        selected_assignment = get_object_or_404(CompanyClientAssignment, pk = assign_id)
        clusters = AssignmentCluster.objects.filter(assignment = selected_assignment.assignment)
        cluster_ids  = []
        question_ids = []
        for cluster in clusters:
            cluster_ids.append(str(cluster.id))
        if request.POST:
            cluster_id       = request.GET.get('cluster_id')
            question_id   = request.GET.get('question_id')
            answer = request.GET.get('answer')
            valuble_answer = AssignmentQuestionAnswer.objects.get(assignment_question__id = question_id, option = answer)
    
            client_assignment = ClientAssignment.objects.create(assignment     =  selected_assignment,
                                                                 cluster_id   =  cluster_id,
                                                                 question_id  =  question_id,
                                                                 client_answer =  answer,
                                                                 status        =  valuble_answer.answer,
                                                                )
            client_assignment.save()
            if valuble_answer.answer:
                clus_position = cluster_ids.index(cluster_id)
                if clus_position == (len(cluster_ids)-1):
                    CompanyClientAssignment.objects.filter(id = assign_id).update(post_status = True, post_read_status = True)
                    messages.success(request,(_("You Successfully Completed this Assignment")),fail_silently = True)
                    return redirect(reverse('client_assignment_list', kwargs={'domain_name': domain_name }))
                else:    
                    next_clus_id =  cluster_ids[clus_position+1]
                    cluster_question = AssignmentQuestion.objects.filter(assignment_cluster__id=next_clus_id)
                    cluster_question = AssignmentQuestion.objects.filter(assignment_cluster__id=next_clus_id)[0]
                    question_answers = AssignmentQuestionAnswer.objects.filter(assignment_question = cluster_question)
                    return render_to_response('client/client_assignment_questions.html', locals(), context_instance = RequestContext(request))
            else:
                cluster_questions = AssignmentQuestion.objects.filter(assignment_cluster__id = cluster_id)
                for cluster_question in cluster_questions:
                    question_ids.append(str(cluster_question.id))
                ques_position = question_ids.index(question_id)
                if ques_position == (len(question_ids)-1):
                    next_ques_id =  question_ids[0]
                else:    
                    next_ques_id =  question_ids[ques_position+1]
                
                cluster_question = AssignmentQuestion.objects.get(id=next_ques_id)
                question_answers = AssignmentQuestionAnswer.objects.filter(assignment_question = cluster_question)
                return render_to_response('client/client_assignment_questions.html', locals(), context_instance = RequestContext(request))
    
        
        exit_assignments = ClientAssignment.objects.filter(assignment = selected_assignment).order_by('-modified_at')
        if exit_assignments:
            exit_assignment = exit_assignments[0]
            if exit_assignment.status:
                clus_position = cluster_ids.index(str(exit_assignment.cluster.id))
                if clus_position == (len(cluster_ids)-1):
                    return redirect(reverse('client_assignment_completed', kwargs={'domain_name': domain_name, 'assign_id':assign_id }))
                else:    
                    next_clus_id =  cluster_ids[clus_position+1]
                    cluster_question = AssignmentQuestion.objects.filter(assignment_cluster__id=next_clus_id)
                    cluster_question = AssignmentQuestion.objects.filter(assignment_cluster__id=next_clus_id)[0]
                    question_answers = AssignmentQuestionAnswer.objects.filter(assignment_question = cluster_question)
                    return render_to_response('client/client_assignment_questions.html', locals(), context_instance = RequestContext(request))
    
            else:
                cluster_questions = AssignmentQuestion.objects.filter(assignment_cluster__id = exit_assignment.cluster.id)
                for cluster_question in cluster_questions:
                    question_ids.append(str(cluster_question.id))
                ques_position = question_ids.index(str(exit_assignment.question.id))
                if ques_position == (len(question_ids)-1):
                    next_ques_id =  question_ids[0]
                else:    
                    next_ques_id =  question_ids[ques_position+1]
    
                cluster_question = AssignmentQuestion.objects.get(id=next_ques_id)
                question_answers = AssignmentQuestionAnswer.objects.filter(assignment_question = cluster_question)
                return render_to_response('client/client_assignment_questions.html', locals(), context_instance = RequestContext(request))
        
        if AssignmentQuestion.objects.filter(assignment_cluster__assignment = selected_assignment.assignment):
            cluster_question = AssignmentQuestion.objects.filter(assignment_cluster__assignment = selected_assignment.assignment)[0]
            question_answers = AssignmentQuestionAnswer.objects.filter(assignment_question = cluster_question)
        else:
            cluster_question = ''
        return render_to_response('client/client_assignment_questions.html', locals(), context_instance = RequestContext(request))
    except CompanyClientAssignment.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_assignment_list', kwargs={'domain_name': domain_name }))
@client_login
def client_assignment_completed(request, domain_name = None, assign_id = None): 
    try:
        assignment = CompanyClientAssignment.objects.get(pk = assign_id)
        selected_assignment = get_object_or_404(CompanyClientAssignment, pk = assign_id)
        exist_feedback = AssignmentFeedback.objects.filter(assignment = assign_id).order_by('created_at')
        assignments = ClientAssignment.objects.filter(assignment = selected_assignment,status = True)
        assignment_name = assignments[0].assignment
        form1 = AssignmentFeedbackForm()
        all_actions = ClientAssignment.objects.filter(assignment = selected_assignment)
        return render_to_response('client/client_assignment_completed.html', locals(), context_instance = RequestContext(request))
    except CompanyClientAssignment.DoesNotExist:
        messages.success(request,(_('This Assignment has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_assignment_list', kwargs={'domain_name': domain_name }))
@client_login
def client_assignment_feedback(request, domain_name = None, assign_id = None):
    try:
        assignment = CompanyClientAssignment.objects.get(pk = assign_id)
        selected_assignment = get_object_or_404(CompanyClientAssignment, pk = assign_id)
        assignments = ClientAssignment.objects.filter(assignment = selected_assignment,status = True)
        assignment_name = assignments[0].assignment
        all_actions = ClientAssignment.objects.filter(assignment = selected_assignment)
        exist_feedback = AssignmentFeedback.objects.filter(assignment = assign_id).order_by('created_at')
        if request.method == "POST":
            form1 = AssignmentFeedbackForm(request.POST, request.FILES)
            if form1.is_valid():
                feedback = form1.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientAssignment.objects.filter(id = assign_id).update(assign_status = False, post_status = True, post_read_status = True)
                
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('client_assignment_list', kwargs={'domain_name': domain_name }))
            else:
                return render_to_response('client/client_assignment_completed.html', locals(), context_instance = RequestContext(request))
            form1 = AssignmentFeedbackForm()     
        return render_to_response('company/client_assignment_completed.html', locals(), context_instance = RequestContext(request))
    except:
        messages.success(request,(_('This Assignment has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_assignment_list', kwargs={'domain_name': domain_name }))