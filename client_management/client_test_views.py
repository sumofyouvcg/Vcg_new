from django.shortcuts import render_to_response, RequestContext
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _

from vcg.company_management.models import CompanyClientTest
from vcg.admin_management.models import TestQuestion, TestRange, TestQuestionAnswers
from vcg.client_management.models import ClientTestAnswers, ClientTestResult, TestFeedback
from vcg.client_management.client_test_forms import TestFeedbackForm
from vcg.utilities import client_login
from vcg.config import choices

@client_login
def test_list(request, domain_name = None):   
    test_list = CompanyClientTest.objects.filter(client__client_number = request.user.username, active = True)
    
    paginate  = Paginator(test_list, choices.list_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        test_list = paginate.page(page)
    except (EmptyPage, InvalidPage):
        test_list = paginate.page(paginate.num_pages)
    num_pages = range(test_list.paginator.num_pages)    
    return render_to_response('client/client_test_list.html', locals(), context_instance = RequestContext(request))

@client_login
def test_details(request, domain_name = None, test_id = None):
    CompanyClientTest.objects.filter(id = test_id).update(assign_status = False)
    try:
        company_test = CompanyClientTest.objects.get(id = test_id)
        questions    = TestQuestion.objects.filter(test = company_test.test)
        answers      = TestQuestionAnswers.objects.filter(question__test = company_test.test)
        test_result  = ClientTestResult.objects.filter(test = company_test)

        if test_result:
            return redirect(reverse('client_test_completed', kwargs={'domain_name': domain_name, 'test_id' : test_id}))

        if request.POST:
            totalscore = 0;
            for each in request.POST:
                if 'radio' in str(each):
                    question_id = int(str(each).split('radio')[1])
                    score       = int(request.POST[each])
                    question    = TestQuestion.objects.get(id = question_id)
                    ClientTestAnswers.objects.create(test        = company_test,
                                                     question    = question.question,
                                                     score       = score,
                                                     created_by  = request.user,
                                                     modified_by = request.user,
                                                     )
                    totalscore += score
            
            test_ranges  = TestRange.objects.filter(test = company_test.test)
            count = 0
            for test_range in test_ranges:
                if test_range.from_value <= totalscore and totalscore <= test_range.to_value:
                    count += 1
                    ClientTestResult.objects.create(
                                                    test   = company_test,
                                                    score  = totalscore,
                                                    result = test_range.result,
                                                    )
            if not count:
                ClientTestResult.objects.create(test   = company_test,
                                                score  = totalscore,
                                                result = "Test Range Not Defined",
                                                )        
            CompanyClientTest.objects.filter(id = test_id).update(post_status = True, post_read_status = True)
            return redirect(reverse('client_test_list', kwargs={'domain_name': domain_name}))
        return render_to_response('client/client_test_questions.html', locals(), context_instance = RequestContext(request))
    except CompanyClientTest.DoesNotExist:
        messages.success(request,(_('This Test has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_test_list', kwargs={'domain_name': domain_name}))
    
@client_login
def client_test_completed(request, domain_name = None, test_id = None): 
    try:
        test           = CompanyClientTest.objects.get( pk = test_id)   
        selected_test  = get_object_or_404(CompanyClientTest, pk = test_id)
        exist_feedback = TestFeedback.objects.filter(test = test_id).order_by('created_at')
        questions      = ClientTestAnswers.objects.filter(test = selected_test)
        answers        = TestQuestionAnswers.objects.filter(question__test = selected_test)
        all_actions    = ClientTestResult.objects.filter(test = selected_test)    

        form1 = TestFeedbackForm()
        return render_to_response('client/client_test_completed.html', locals(), context_instance = RequestContext(request))

    except CompanyClientTest.DoesNotExist:
        messages.success(request,(_('This Test has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_test_list', kwargs={'domain_name': domain_name}))

@client_login
def client_test_feedback(request, domain_name = None, test_id = None):
    try:
        test = CompanyClientTest.objects.get( pk = test_id)  
        selected_test = get_object_or_404(CompanyClientTest, pk = test_id)
        questions = ClientTestAnswers.objects.filter(test = selected_test)
        all_actions = ClientTestResult.objects.filter(test = selected_test)
        exist_feedback = TestFeedback.objects.filter(test = test_id).order_by('created_at')
        if request.method == "POST":
            form1 = TestFeedbackForm(request.POST, request.FILES)
            if form1.is_valid():
                feedback = form1.save(commit = False)
                feedback.created_by = feedback.modified_by = request.user
                feedback.active = True
                feedback.save()
                
                CompanyClientTest.objects.filter(id = test_id).update(assign_status = False, post_status = True, post_read_status = True)
                 
                messages.success(request,(_("Your Feedback Sent Successfully")),
                                             fail_silently = True)
                return redirect(reverse('client_test_list', kwargs={'domain_name': domain_name}))
            else:
                return render_to_response('client/client_test_completed.html', locals(), context_instance = RequestContext(request))
            form1 = TestFeedbackForm()     
        return render_to_response('company/client_test_completed.html', locals(), context_instance = RequestContext(request))
    except CompanyClientTest.DoesNotExist:
        messages.success(request,(_('This Test has been removed by Company')), fail_silently= True)
        return redirect(reverse('client_test_list', kwargs={'domain_name': domain_name}))