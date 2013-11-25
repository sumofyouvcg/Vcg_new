from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from vcg.util.models import Audit
from vcg.admin_management.models import CreateQuestion, Client, AssignmentCluster, AssignmentQuestion, Company
from vcg.company_management.models import CompanyClientPlan, CompanyClientTest, CompanyClientAssignment, CompanyClientTreatment, CompanyClientDiary, CompanyClientAnimation, CompanyForms
from django_countries import CountryField
from vcg.config.choices import gender
from vcg.config.forms import marital_status, live, change_living_environment, genaral_feel_number, terms_conditions, contents_sessions, online_therapy, client_consultation, methods_techniques, treat_domains, domains_yes, indicator_treatment

class ClientPlan(Audit):
    plan                        = models.ForeignKey(CompanyClientPlan, verbose_name = _('Plan'))
    action                      = models.CharField(max_length = 50, verbose_name = _('Action*'))
    description                 = models.TextField(max_length = 500, verbose_name = _('Description*'))
    achieved                    = models.CharField(max_length = 3, verbose_name = _('Achieved*'))
   
    def __unicode__(self):
        return u' %s' % (self.plan)

    class Meta:
        verbose_name            = _('Plan')
        verbose_name_plural     = _('Plans')
        
    def save(self, *args, **kwargs): 
        super(ClientPlan, self).save( *args, **kwargs)

class PlanFeedback(Audit):
    plan                        = models.ForeignKey(CompanyClientPlan, verbose_name = _('Plan'))
    feedback                    = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))
   
    def __unicode__(self):
        return u' %s' % (self.plan)

    class Meta:
        verbose_name            = _('PlanFeedback')
        verbose_name_plural     = _('PlanFeedbacks')
        
    def save(self, *args, **kwargs): 
        super(PlanFeedback, self).save( *args, **kwargs)

class ClientTestAnswers(Audit):
    test     = models.ForeignKey(CompanyClientTest)
    question = models.CharField('Question', max_length = 150)
    score    = models.CharField(max_length = 3)

    def __unicode__(self):
        return self.question

class ClientTestResult(Audit):
    test   = models.ForeignKey(CompanyClientTest)
    score  = models.CharField(max_length = 3)
    result = models.CharField(max_length = 150)

    def __unicode__(self):
        return self.result

class TestFeedback(Audit):
    test     = models.ForeignKey(CompanyClientTest)
    feedback = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))

    def __unicode__(self):
        return self.feedback

class ClientQuestionsAnswers(Audit):
    client_question_id  = models.CharField(max_length = 100)
    module              = models.ForeignKey(CompanyClientTreatment)
    question_text       = models.CharField(max_length = 100)
    help_text           = models.CharField(max_length = 50)
    answer_type         = models.CharField(max_length = 20)
    answer              = models.CharField(max_length = 1000, null= True, blank = True)
    min_value           = models.PositiveIntegerField(max_length = 150, null= True, blank = True)
    max_value           = models.PositiveIntegerField(max_length = 150, null= True, blank = True)
    exact_answer        = models.CharField(max_length = 500)
    client              = models.ForeignKey(Client)
    
    def __unicode__(self):
        return self.question_text
    
class ClientQuestions(Audit):
    client_treatment    = models.ForeignKey(CompanyClientTreatment)
    question            = models.ForeignKey(CreateQuestion)
    answer              = models.CharField(max_length = 500)
    client              = models.ForeignKey(Client)
    
    def __unicode__(self):
        return self.question.question_text
    
class ClientQuestionsFeedback(Audit):
    client_treatment    = models.ForeignKey(CompanyClientTreatment)
    feedback            = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))
    client              = models.ForeignKey(Client)

    def __unicode__(self):
        return self.feedback
    
class ClientAssignment(Audit):
    assignment     = models.ForeignKey(CompanyClientAssignment)
    cluster        = models.ForeignKey(AssignmentCluster)
    question       = models.ForeignKey(AssignmentQuestion)
    client_answer  = models.CharField(max_length = 100)
    status         = models.BooleanField(default = False)
   
    def __unicode__(self):
        return u' %s' % (self.assignment)

    class Meta:
        verbose_name            = _('Assignment')
        verbose_name_plural     = _('Assignments')
        
    def save(self, *args, **kwargs): 
        super(ClientAssignment, self).save( *args, **kwargs)    
        
class AssignmentFeedback(Audit):
    assignment                  = models.ForeignKey(CompanyClientAssignment)
    feedback                    = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))
   
    def __unicode__(self):
        return u' %s' % (self.assignment)

    class Meta:
        verbose_name            = _('AssignmentFeedback')
        verbose_name_plural     = _('AssignmentFeedbacks')
        
    def save(self, *args, **kwargs): 
        super(AssignmentFeedback, self).save( *args, **kwargs)
        
class ClientDiary(Audit):
    diary               = models.ForeignKey(CompanyClientDiary)
    client_question_id  = models.CharField(max_length = 100)
    question            = models.CharField(max_length = 100)
    help_text           = models.CharField(max_length = 50)
    answer_type         = models.CharField(max_length = 20)
    answer_options      = models.CharField(max_length = 1000, null= True, blank = True)
    min_value           = models.PositiveIntegerField(max_length = 150, null= True, blank = True)
    max_value           = models.PositiveIntegerField(max_length = 150, null= True, blank = True)
    exact_answer        = models.CharField(max_length = 500)
    date                = models.DateField()
    
    def __unicode__(self):
        return self.question       
    
class DiaryFeedback(Audit):
    diary                       = models.ForeignKey(CompanyClientDiary, verbose_name = _('Plan'))
    date                        = models.DateField()
    feedback                    = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))
   
    def __unicode__(self):
        return u' %s' % (self.diary)

    class Meta:
        verbose_name            = _('DiaryFeedback')
        verbose_name_plural     = _('DiaryFeedbacks')
        
    def save(self, *args, **kwargs): 
        super(DiaryFeedback, self).save( *args, **kwargs)


class AnimationFeedback(Audit):
    animation                   = models.ForeignKey(CompanyClientAnimation, verbose_name = _('Animation'))
    feedback                    = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))
   
    def __unicode__(self):
        return u' %s' % (self.animation)

    class Meta:
        verbose_name            = _('AnimationFeedback')
        verbose_name_plural     = _('AnimationFeedbacks')
        
    def save(self, *args, **kwargs): 
        super(AnimationFeedback, self).save( *args, **kwargs)
    
class ChatMessage(models.Model):
    sender          = models.ForeignKey(User, related_name = 'sender_user')
    receiver        = models.ForeignKey(User, related_name = 'receiver_user')
    message         = models.CharField(max_length = 200)
    received_at     = models.DateTimeField(auto_now_add = True)
    #session         = models.ForeignKey(Session)
    is_read         = models.BooleanField()

class LastActive(models.Model):    
    user            = models.OneToOneField(User)
    received_at     = models.DateTimeField(auto_now = True)
    session         = models.ForeignKey(Session)
    
class ClientIntakeForm1(Audit):
    name                        = models.CharField(max_length = 500, verbose_name = _('Name*'))
    birth_name                  = models.CharField(max_length = 500, verbose_name = _('Birth Name*'))
    first_name                  = models.CharField(max_length = 500, verbose_name = _('First names (in full)*'))
    nick_name                   = models.CharField(max_length = 500, verbose_name = _('Nickname*'))
    address                     = models.CharField(max_length = 500, verbose_name = _('Street and house number*'))
    postal_code_city            = models.CharField(max_length = 500, verbose_name = _('Postal code and City*'))
    phone_number                = models.CharField(max_length = 500, verbose_name = _('Telephone number (s)*'))
    email                       = models.EmailField(verbose_name = _('E-Mail address*'))
    dob                         = models.DateField(verbose_name = _('Date of birth*'))
    gender                      = models.CharField(max_length = 500, choices = gender, verbose_name = _('Sex*'))
    marital_status              = models.CharField(max_length = 500, choices = marital_status, verbose_name = _('Marital status*'))
    home                        = models.CharField(max_length = 500, verbose_name = _('Home*'))
    citizen_service_number      = models.CharField(max_length = 500, verbose_name = _('Citizen Service Number*'))
    health_insurance_number     = models.CharField(max_length = 500, verbose_name = _('Health insurance company and policy number*'))
    doctor_name                 = models.CharField(max_length = 500, verbose_name = _('Name of the doctor*'))
    telephone_gp                = models.CharField(max_length = 500, verbose_name = _('Telephone GP*'))

    live                        = models.CharField(max_length = 50, choices = live, verbose_name = _('Do you live alone or with others*'))
    change_living_environment   = models.CharField(max_length = 50, choices = change_living_environment, verbose_name = _('Would have to change something to your living environment*'))
    
    partner_details             = models.TextField(max_length = 150, verbose_name = _('You have a partner, how long, how is your relationship?'), null = True, blank = True)
    children_details            = models.TextField(max_length = 150, verbose_name = _('Have children (number, gender, age)?'), null = True, blank = True)
    about_relationship          = models.TextField(max_length = 150, verbose_name = _('How is your relationship with them?'), null = True, blank = True)
    friends_details             = models.TextField(max_length = 150, verbose_name = _('Do you have friends and / or acquaintances, what is the relationship?'), null = True, blank = True)
    main_name                   = models.TextField(max_length = 150, verbose_name = _('Who is the main man for you?'), null = True, blank = True)
    
    profession                  = models.CharField(max_length = 500, verbose_name = _('What is your profession*'))
    working_hours               = models.CharField(max_length = 500, verbose_name = _('How many hours a week you work*'))
    steady_income               = models.CharField(max_length = 500, verbose_name = _('You have a steady income?*'))
    benefit                     = models.CharField(max_length = 500, verbose_name = _('Have a benefit, if so which one?*'))
    provides_other_people       = models.CharField(max_length = 500, verbose_name = _('Provides for other people?*'))
    household_chores            = models.CharField(max_length = 500, verbose_name = _('Doing household chores?*'))
    free_time                   = models.CharField(max_length = 500, verbose_name = _('How much free time do you have?*'))
    free_time_hobbies           = models.CharField(max_length = 500, verbose_name = _('What you enjoy doing in your free time?*'))
    
    problem                     = models.TextField(max_length = 1000, verbose_name = _('What is your problem?'), null = True, blank = True)
    problem_duration            = models.TextField(max_length = 1000, verbose_name = _('How old is your problem?'), null = True, blank = True)
    event_advance               = models.TextField(max_length = 1000, verbose_name = _('Is there an event gone to advance?'), null = True, blank = True)
    
    cause_problem               = models.TextField(max_length = 1000, verbose_name = _('What is the cause of your problem?'), null = True, blank = True)
    people_involved             = models.CharField(max_length = 500, verbose_name = _('Are there other people involved?*'))
    your_share                  = models.TextField(max_length = 1000, verbose_name = _('What is your share?'), null = True, blank = True)
    their_share                 = models.TextField(max_length = 1000, verbose_name = _('What is their share?'), null = True, blank = True)
    
    suffer_problem_count        = models.TextField(max_length = 1000, verbose_name = _('How many are suffering from the problem?'), null = True, blank = True)
    feel_location               = models.TextField(max_length = 1000, verbose_name = _('Where do you feel that especially?'), null = True, blank = True)
    like_to_change              = models.TextField(max_length = 1000, verbose_name = _('What would you like to change?'), null = True, blank = True)
    genaral_feel_number         = models.CharField(max_length = 500, choices = genaral_feel_number, verbose_name = _('General feeling of well-being? Enter a number between 0 and 10.'), null = True, blank = True)
    
    way_of_thinking             = models.TextField(max_length = 1000, verbose_name = _('How the problem affects your way of thinking?'), null = True, blank = True)
    emotional_life              = models.TextField(max_length = 1000, verbose_name = _('How the problem affects your emotional life?'), null = True, blank = True)
    behaviour                   = models.TextField(max_length = 1000, verbose_name = _('How the problem affects your behavior?'), null = True, blank = True)
    
    already_tried               = models.TextField(max_length = 1000, verbose_name = _('What have you already tried?'), null = True, blank = True)
    differnce                   = models.TextField(max_length = 1000, verbose_name = _('Have you made a difference?'), null = True, blank = True)
    want_to_try                 = models.TextField(max_length = 1000, verbose_name = _('What more could you want to try?'), null = True, blank = True)
    
    therapy                     = models.TextField(max_length = 1000, verbose_name = _('Are you in therapy?'), null = True, blank = True)
    duration                    = models.CharField(max_length = 500, verbose_name = _('If so, when (from - to) and how often?*'))
    who_was_that                = models.CharField(max_length = 500, verbose_name = _('Who was that?*'))
    what_problem                = models.TextField(max_length = 1000, verbose_name = _('What was the problem?'), null = True, blank = True)
    therapy_outcome             = models.CharField(max_length = 500, verbose_name = _('Has had the therapy outcome?*'))
    finding_solution            = models.TextField(max_length = 1000, verbose_name = _('What hinders you in finding a solution?'), null = True, blank = True)
    
    
    keeps_on_leg                = models.CharField(max_length = 500, verbose_name = _('What keeps you on the leg?*'))
    get_energy                  = models.CharField(max_length = 500, verbose_name = _('Where do you get energy?*'))
    where_satisfied             = models.CharField(max_length = 500, verbose_name = _('Where are you satisfied?*'))
    good_in_your_life           = models.CharField(max_length = 500, verbose_name = _('What going to (do) good in your life?*'))
    
    someone_your_problem        = models.CharField(max_length = 500, verbose_name = _('Can someone with your problem?*'))
    anyone_you_support          = models.CharField(max_length = 500, verbose_name = _('Is there anyone that you support?*'))
    height_of_problem           = models.CharField(max_length = 500, verbose_name = _('Is the one on the height of your problem?*'))
    you_smoke                   = models.CharField(max_length = 500, verbose_name = _('Do you smoke, if so what and how much?*'))
    
    
    carry_out_work              = models.CharField(max_length = 500, verbose_name = _('You can carry out your work?*'))
    relation_with_others        = models.CharField(max_length = 500, verbose_name = _('Are your relationships with others?*'))
    meaning_in_life             = models.CharField(max_length = 500, verbose_name = _('You still have meaning in life?*'))
    interest_in_things          = models.CharField(max_length = 500, verbose_name = _('You have interest in things?*'))
    meet_expectations           = models.CharField(max_length = 500, verbose_name = _('You can meet your own expectations?*'))
    about_future                = models.TextField(max_length = 1000, verbose_name = _('How do you see the future?'), null = True, blank = True)

class ClientIntakeForm2(Audit):    
    physical_problems           = models.CharField(max_length = 500, verbose_name = _('Have any physical problems?*'))
    medical_conditions          = models.CharField(max_length = 500, verbose_name = _('You have a medical condition?*'))
    about_medication            = models.CharField(max_length = 500, verbose_name = _('You are taking medication, if so which ones and in what dosage?*'))
    about_drugs                 = models.CharField(max_length = 500, verbose_name = _('You use drugs, if so which ones and how much?*'))
    about_alcohol               = models.CharField(max_length = 500, verbose_name = _('You drink alcohol, if so how much per day?*'))
    about_smoke                 = models.CharField(max_length = 500, verbose_name = _('Do you smoke, if so what and how much?*'))
    eating_disorders            = models.CharField(max_length = 500, verbose_name = _('Have eating disorders?*'))
    sleep_problem               = models.CharField(max_length = 500, verbose_name = _('Do you have sleep problems?*'))
    sexually_active             = models.CharField(max_length = 500, verbose_name = _('Are you sexually active?*'))
    
    accomplish                  = models.TextField(max_length = 1000, verbose_name = _('What would you like to accomplish with the therapy?'), null = True, blank = True)
    effect                      = models.TextField(max_length = 1000, verbose_name = _('What effects you expect from it?'), null = True, blank = True)
    most_important              = models.TextField(max_length = 1000, verbose_name = _('What is the most important for you?'), null = True, blank = True)
    life_look                   = models.CharField(max_length = 500, verbose_name = _('What does your life look like if you have it?*'))
    when_achieved               = models.CharField(max_length = 500, verbose_name = _('When would you like to have achieved?*'))
    what_tasks                  = models.TextField(max_length = 1000, verbose_name = _('What tasks do you see for me?'), null = True, blank = True)
    
    parents_details             = models.CharField(max_length = 500, verbose_name = _('Are your parents alive (how old are they)?*'))
    family_children_details     = models.CharField(max_length = 500, verbose_name = _('How many children were in your family of origin?*'))
    chile_in_line               = models.CharField(max_length = 500, verbose_name = _('What child in line was?*'))    
    child_temperament           = models.CharField(max_length = 500, verbose_name = _('What was for a child (temperament)?*'))
    easy_contact                = models.CharField(max_length = 500, verbose_name = _('Made you easy to contact?*'))
    like_as_child               = models.TextField(max_length = 1000, verbose_name = _('What did you like as a child?'), null = True, blank = True)
    material_conditions         = models.CharField(max_length = 500, verbose_name = _('How were the material conditions?*'))
    emotional_conditions        = models.TextField(max_length = 1000, verbose_name = _('How were the emotional conditions?'), null = True, blank = True)
    father                      = models.TextField(max_length = 1000, verbose_name = _('What was your father for a man?'), null = True, blank = True)
    style_of_parenting          = models.TextField(max_length = 1000, verbose_name = _('What was his style of parenting?'), null = True, blank = True)
    father_occupation           = models.CharField(max_length = 500, verbose_name = _('What he did for a living?*'))
    father_relationship         = models.TextField(max_length = 1000, verbose_name = _('How was your relationship with him?'), null = True, blank = True)
    mother                      = models.TextField(max_length = 1000, verbose_name = _('What was your mother for a woman?'), null = True, blank = True)
    untitled_element            = models.TextField(max_length = 1000, verbose_name = _('untitled element'), null = True, blank = True)
    mother_occupation           = models.CharField(max_length = 500, verbose_name = _('What did she do for work?*'))
    mother_relationship         = models.TextField(max_length = 1000, verbose_name = _('How was your relationship with her?'), null = True, blank = True)
    parents_eye_desires         = models.TextField(max_length = 1000, verbose_name = _('Your parents had an eye for your desires?'), null = True, blank = True)
    parents_relationship        = models.TextField(max_length = 1000, verbose_name = _('How was the relationship between your parents?'), null = True, blank = True)
    important_in_youth          = models.CharField(max_length = 500, verbose_name = _('Who was the most important in your youth?*')) 
    cultural_background         = models.CharField(max_length = 500, verbose_name = _('Cultural background / emi-immigration?*'))
    
    family_involvement          = models.CharField(max_length = 500, verbose_name = _('The family members were involved in?*'))
    support                     = models.CharField(max_length = 500, verbose_name = _('Who did you support as a child?*'))
    warmth_love                 = models.CharField(max_length = 500, verbose_name = _('Who gave you warmth and love?*'))
    home_for_saying             = models.CharField(max_length = 500, verbose_name = _('Who had it at home for saying?*'))
    responsibility              = models.CharField(max_length = 500, verbose_name = _('Who took the responsibility?*'))
    decisions                   = models.CharField(max_length = 500, verbose_name = _('Who made the decisions?*'))
    bepreken                    = models.CharField(max_length = 500, verbose_name = _('You could as a child all bepreken?*'))
    religion_role               = models.CharField(max_length = 500, verbose_name = _('Religion played a role in the family?*'))
    about_freedom               = models.CharField(max_length = 500, verbose_name = _('How much freedom you had as a child?*'))
    labor_division              = models.CharField(max_length = 500, verbose_name = _('How was the division of labor in your family?*'))
    family_tasks                = models.CharField(max_length = 500, verbose_name = _('Had also tasks in the family?*'))
    
    physical_violence           = models.CharField(max_length = 500, verbose_name = _('Do you have experience with physical violence?*'))
    mental_violenc              = models.CharField(max_length = 500, verbose_name = _('Do you have experience with mental violence?*'))
    sexual_violence             = models.CharField(max_length = 500, verbose_name = _('Do you have experience with sexual violence?*'))
    childhood                   = models.CharField(max_length = 500, verbose_name = _('How was your childhood?*'))
    bullied_in_childhood        = models.CharField(max_length = 500, verbose_name = _('Are you being bullied in your childhood?*'))
    adolescence                 = models.CharField(max_length = 500, verbose_name = _('How was your adolescence?*'))
    accepted_youth              = models.CharField(max_length = 500, verbose_name = _('How were you accepted in your youth?*'))
    pleasant_memory             = models.CharField(max_length = 500, verbose_name = _('What is your most pleasant memory?*'))
    nastiest_memory             = models.CharField(max_length = 500, verbose_name = _('What is your nastiest memory?*'))

class ClientIntakeForm3(Audit):    
    commandments_youth          = models.CharField(max_length = 500, verbose_name = _('Which commandments were in your youth?*'))
    prohibited_youth            = models.CharField(max_length = 500, verbose_name = _('Which were prohibited in your youth?*'))
    informed_sexually           = models.CharField(max_length = 500, verbose_name = _('Are you informed sexually?*'))
    handle_conflicts            = models.CharField(max_length = 500, verbose_name = _('How did they handle conflicts?*'))
    affection_shown             = models.CharField(max_length = 500, verbose_name = _('How was affection shown?*'))
    standards_values            = models.CharField(max_length = 500, verbose_name = _('What were the standards and values in your family?*'))
    
    school                      = models.CharField(max_length = 500, verbose_name = _('How was your school?*'))
    highest_education           = models.CharField(max_length = 500, verbose_name = _('What is your highest level of education?*'))
    training                    = models.CharField(max_length = 500, verbose_name = _('Was free in the choice of your training?*'))
    encouraged_parents          = models.CharField(max_length = 500, verbose_name = _('Were you encouraged by your parents?*'))
    talents                     = models.CharField(max_length = 500, verbose_name = _('They had an eye for your talents?*')) 
    forced_direction            = models.CharField(max_length = 500, verbose_name = _('Was forced in one direction?*')) 
    contacts_at_school          = models.CharField(max_length = 500, verbose_name = _('How were your contacts at school?*'))
    contacts_with_friends       = models.CharField(max_length = 500, verbose_name = _('How were your contacts with friends?*')) 
    your_hobbies                = models.CharField(max_length = 500, verbose_name = _('What were your hobbies?*'))    
    clubs_associations          = models.CharField(max_length = 500, verbose_name = _('Were you a member of clubs or associations*'))
    satisfied_education         = models.CharField(max_length = 500, verbose_name = _('Are you satisfied with your education?*'))
    satisfied_work              = models.CharField(max_length = 500, verbose_name = _('Are you satisfied with your current work?*'))
    
    terms_conditions            = models.CharField(max_length = 50, choices = terms_conditions, verbose_name = _('Do you agree with the terms and conditions of the practitioner (see menu item "Terms")?*'))
    finance_therapy             = models.CharField(max_length = 500, verbose_name = _('You finance the therapy itself?*'))
    
    comments                    = models.TextField(max_length = 1000, verbose_name = _('Other comments and / or questions'), null = True, blank = True)

class ClientIntakeForm(Audit):
    client                      = models.ForeignKey(Client)
    company_forms               = models.ForeignKey(CompanyForms)
    form1                       = models.ForeignKey(ClientIntakeForm1)
    form2                       = models.ForeignKey(ClientIntakeForm2)
    form3                       = models.ForeignKey(ClientIntakeForm3)
   
    def __unicode__(self):
        return u' %s' % (self.company_forms)
    
    def save(self, *args, **kwargs): 
        super(ClientIntakeForm, self).save( *args, **kwargs)
        
class CompanyFormFeedback(Audit):
    client_intake_form          = models.ForeignKey(ClientIntakeForm, verbose_name = _('Form'))
    feedback                    = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))
   
    def __unicode__(self):
        return u' %s' % (self.client_intake_form)
    
    def save(self, *args, **kwargs): 
        super(CompanyFormFeedback, self).save( *args, **kwargs)
        
class TreatmentAgreement(Audit):
    client_name                 = models.CharField(max_length = 500, verbose_name = _('Name Client'), null = True, blank = True)
    address                     = models.CharField(max_length = 500, verbose_name = _('Address'), null = True, blank = True)
    code_town                   = models.TextField(max_length = 1000, verbose_name = _('Code and Town'), null = True, blank = True)
    dob                         = models.DateField(verbose_name = _('Date of Birth'), null = True, blank = True)
    bsn_number                  = models.CharField(max_length = 500, verbose_name = _('BSN Number'), null = True, blank = True)
    date_treatment_agreement    = models.CharField(max_length = 500, verbose_name = _('Date Occlusion Treatment Agreement:'), null = True, blank = True)
    treatment_goal              = models.TextField(max_length = 1000, verbose_name = _('Main Treatment Goal (s):'), null = True, blank = True)
    notes                       = models.TextField(max_length = 1000, verbose_name = _('Notes'), null = True, blank = True)
    contents_sessions           = models.CharField(max_length = 500, choices = contents_sessions, verbose_name = _('Contents sessions'), null = True, blank = True)
    online_therapy              = models.CharField(max_length = 500, choices = online_therapy, verbose_name = _('Online therapy'), null = True, blank = True)
    client_consultation         = models.CharField(max_length = 500, choices = client_consultation, verbose_name = _('During the sessions, in consultation with the client make use of one or more of the following methods and / or applications.'), null = True, blank = True)


class ClientTreatmentAgreementForm(Audit):
    client                      = models.ForeignKey(Client)
    company_forms               = models.ForeignKey(CompanyForms)
    treatment_agreement         = models.ForeignKey(TreatmentAgreement)
   
    def __unicode__(self):
        return u' %s' % (self.company_forms)
    
    def save(self, *args, **kwargs): 
        super(ClientTreatmentAgreementForm, self).save( *args, **kwargs)
        
class TreatmentAgreementFeedback(Audit):
    client_treatment_agreement_form         = models.ForeignKey(ClientTreatmentAgreementForm, verbose_name = _('Form'))
    feedback                                = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))
   
    def __unicode__(self):
        return u' %s' % (self.client_treatment_agreement_form)
    
    def save(self, *args, **kwargs): 
        super(TreatmentAgreementFeedback, self).save( *args, **kwargs)
        
class MethodsTechniques(Audit):
    methods_tech = models.CharField(max_length = 500, choices = methods_techniques, verbose_name = _('Which methods and techniques?'), null = True, blank = True)
    
    def save(self, *args, **kwargs): 
        super(MethodsTechniques, self).save( *args, **kwargs)
        
class DomainYes(Audit):
    domain = models.CharField(max_length = 100, choices = domains_yes, verbose_name = _('If yes, which'), null = True, blank = True)
    
    def save(self, *args, **kwargs): 
        super(DomainYes, self).save( *args, **kwargs)
        
class IndicatorTreatment(Audit):
    indicator_treat = models.CharField(max_length = 100, choices = indicator_treatment, verbose_name = _('Indicator treatment duration'), null = True, blank = True)
    
    def save(self, *args, **kwargs): 
        super(IndicatorTreatment, self).save( *args, **kwargs)
    
class TreatmentForm(Audit):
    client_name                 = models.CharField(max_length = 500, verbose_name = _('Client Name'), null = True, blank = True)
    address                     = models.CharField(max_length = 500, verbose_name = _('Address'), null = True, blank = True)
    code_town                   = models.TextField(max_length = 1000, verbose_name = _('Code and Town'), null = True, blank = True)
    dob                         = models.DateField(verbose_name = _('Date of Birth'), null = True, blank = True)
    bsn_number                  = models.CharField(max_length = 500, verbose_name = _('BSN Number'), null = True, blank = True)
    date_treatment_agreement    = models.CharField(max_length = 500, verbose_name = _('Date Occlusion Treatment Agreement:'), null = True, blank = True)
    treatment_goal              = models.TextField(max_length = 1000, verbose_name = _('Main Treatment Goal (s):'), null = True, blank = True)
    notes                       = models.TextField(max_length = 1000, verbose_name = _('Notes'), null = True, blank = True)
    contents_sessions           = models.CharField(max_length = 500, choices = contents_sessions, verbose_name = _('Contents sessions'), null = True, blank = True)
    online_therapy              = models.CharField(max_length = 500, choices = online_therapy, verbose_name = _('Online therapy'), null = True, blank = True)
    client_consultation         = models.CharField(max_length = 500, choices = client_consultation, verbose_name = _('During the sessions, in consultation with the client make use of one or more of the following methods and / or applications.*'), null = True, blank = True)
    methods_techniques          = models.ManyToManyField(MethodsTechniques)
    treat_domains               = models.CharField(max_length = 100, choices = treat_domains, verbose_name = _('Can treat domains are distinguished'), null = True, blank = True)
    domains_yes                 = models.ManyToManyField(DomainYes)
    specific_beliefs            = models.TextField(max_length = 1000, verbose_name = _('Are there any specific beliefs or life experiences which are analyzed in the treatment or gedesentiseerd?'), null = True, blank = True)
    indicator_treatment         = models.ManyToManyField(IndicatorTreatment)
    one_three_sessions          = models.TextField(max_length = 1000, verbose_name = _('1-3 sessions'), null = True, blank = True)
    three_nine_sessions         = models.TextField(max_length = 1000, verbose_name = _('3-9 sessions'), null = True, blank = True)
    less_nine_sessions          = models.TextField(max_length = 1000, verbose_name = _('<9 sessions'), null = True, blank = True)
    after_care_treatment        = models.TextField(max_length = 1000, verbose_name = _('After completion of treatment, we agree that there will if necessary be soon a follow up appointment can be made. (By phone within two weeks)'), null = True, blank = True)
    
    def save(self, *args, **kwargs): 
        super(TreatmentForm, self).save( *args, **kwargs)
        
class CompanyTreatmentForm(Audit):
    client                      = models.ForeignKey(Client)
    company_forms               = models.ForeignKey(CompanyForms)
    treatment_form              = models.ForeignKey(TreatmentForm)
    
    def __unicode__(self):
        return u' %s' % (self.company_forms)
    
    def save(self, *args, **kwargs): 
        super(CompanyTreatmentForm, self).save( *args, **kwargs)
        
class CompanyTreatmentFormFeedback(Audit):
    company_treatment_form      = models.ForeignKey(CompanyTreatmentForm, verbose_name = _('Form'))
    feedback                    = models.TextField(max_length = 1000, verbose_name = _('Feedback'))
   
    def __unicode__(self):
        return u' %s' % (self.company_treatment_form)
    
    def save(self, *args, **kwargs): 
        super(CompanyTreatmentFormFeedback, self).save( *args, **kwargs)