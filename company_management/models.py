from django.db import models

from django_countries import CountryField
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from vcg.config.forms import form_names
from vcg.config.choices import treatment_guidence, diary_intervel, continents
from vcg.admin_management.models import Company, Caregiver, Client, Plan, Diary, Session,CompanyModules, Assignment, Test, Module, Animation
from vcg.util.models import Audit

class ClientCaregivers(Audit):
    client                      = models.ForeignKey(Client, verbose_name = _('Client*'))
    caregiver                   = models.ForeignKey(Caregiver, verbose_name = _('Caregiver*'))
    task_id                     = models.CharField(max_length = 50, verbose_name = _('Task Id*'))
    
    def __unicode__(self):
        return u' %s' % (self.caregiver)
    
class CompanyClientPlan(Audit):
    client                      = models.ForeignKey(Client, verbose_name = _('Client*'))
    caregiver                   = models.ForeignKey(Caregiver, verbose_name = _('Caregiver*'))
    practise_plan               = models.ForeignKey(Plan, verbose_name = _('Plan*'))
    goal                        = models.CharField(max_length = 50, verbose_name = _('Goal*'))
    description                 = models.TextField(max_length = 500, verbose_name = _('Description*'))
    goal_achieved               = models.CharField(max_length = 50, verbose_name = _('When the Goal will be Achieved*'))
    active                      = models.BooleanField(default = True, verbose_name = _('Active'))
    assign_status               = models.BooleanField(default = True, verbose_name = _('Assign Status'))
    post_status                 = models.BooleanField(default = False, verbose_name = _('Post Status'))
    post_read_status            = models.BooleanField(default = False, verbose_name = _('Post Read Status'))
    
    def __unicode__(self):
        return u' %s' % (self.practise_plan)

    class Meta:
        verbose_name            = _('Plan')
        verbose_name_plural     = _('Plans')
        
    def save(self, *args, **kwargs): 
        super(CompanyClientPlan, self).save( *args, **kwargs)
  
class CompanyClientTreatment(Audit):
    client                    = models.ForeignKey(Client, verbose_name = _('Client*'))
    module                    = models.ForeignKey(Module, verbose_name = _('Module*'))
    title                     = models.CharField(max_length = 50, verbose_name = _('Title*'))
    caregiver                 = models.ForeignKey(Caregiver, verbose_name = _('Caregiver*'))
    first_session_activation  = models.BooleanField(default = True, verbose_name = _('First Session Activation'))
    guidance                  = models.CharField(max_length = 50, choices = treatment_guidence, verbose_name = _('Guidance*'))
    active                    = models.BooleanField(default = True, verbose_name = _('Active'))
    question_active_status    = models.BooleanField(default = True, verbose_name = _('Question Active Status'))
    question_post_status      = models.BooleanField(default = False, verbose_name = _('Question Post Status'))
    question_post_read_status = models.BooleanField(default = False, verbose_name = _('Question Post Read Status'))
    
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name            = _('CompanyClientTreatment')
        verbose_name_plural     = _('CompanyClientTreatments')
        
    def save(self, *args, **kwargs): 
        super(CompanyClientTreatment, self).save( *args, **kwargs)
        
class ClientTreatmentSessions(Audit):
    client_treatment         = models.ForeignKey(CompanyClientTreatment, verbose_name = _('Client Treatment*'))
    client                   = models.ForeignKey(Client, verbose_name = _('Client*'))
    module                   = models.ForeignKey(Module, verbose_name = _('Module*'))
    sessions                 = models.ForeignKey(Session, verbose_name = _('Sessions*'))
    active                   = models.BooleanField(default = True, verbose_name = _('Active'))
    activate_session         = models.BooleanField(default = False, verbose_name = _('Activate Session'))
    make_unaccompanied       = models.BooleanField(default = False, verbose_name = _('Make Unaccompanied'))
    completed                = models.BooleanField(default = False, verbose_name = _('Unaccompanied'))
    assign_status            = models.BooleanField(default = False, verbose_name = _('Assign Status'))
    post_status              = models.BooleanField(default = False, verbose_name = _('Post Status'))
    post_read_status         = models.BooleanField(default = False, verbose_name = _('Post Read Status'))
    
    def __unicode__(self):
        return self.client.name

    class Meta:
        verbose_name        = _('ClientTreatmentSession')
        verbose_name_plural = _('ClientTreatmentSessions')
        
    def save(self, *args, **kwargs): 
        super(ClientTreatmentSessions, self).save( *args, **kwargs)     
        
class ClientSessionsFeedback(Audit):
    treatment_session        = models.ForeignKey(ClientTreatmentSessions, verbose_name = _('Treatment Session*'))
    client                   = models.ForeignKey(Client, verbose_name = _('Client*'))
    client_treatment         = models.ForeignKey(CompanyClientTreatment, verbose_name = _('Client Treatment*'))
    feedback                 = models.TextField(max_length = 1000, verbose_name = _('Feedback*'))
    active                   = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.client.name

    class Meta:
        verbose_name        = _('ClientSessionsFeedback')
        verbose_name_plural = _('ClientSessionsFeedbacks')
        
    def save(self, *args, **kwargs): 
        super(ClientSessionsFeedback, self).save( *args, **kwargs)                   
        
class CompanyClientDiary(Audit):
    client                      = models.ForeignKey(Client, verbose_name = _('Client*'))
    diary                       = models.ForeignKey(Diary, verbose_name = _('Diary*')) 
    caregiver                   = models.ForeignKey(Caregiver, verbose_name = _('Caregiver*'))  
    intervel                    = models.CharField(max_length = 50, choices = diary_intervel, verbose_name = _('Intervel*'))  
    active                      = models.BooleanField(default = True, verbose_name = _('Active'))           
    assign_status               = models.BooleanField(default = True, verbose_name = _('Assign Status'))
    post_status                 = models.BooleanField(default = False, verbose_name = _('Post Status'))
    post_read_status            = models.BooleanField(default = False, verbose_name = _('Post Read Status'))
    
    def __unicode__(self):
        return u' %s' % (self.diary)

    class Meta:
        verbose_name            = _('ClientDiary')
        verbose_name_plural     = _('ClientDiaries')
        
    def save(self, *args, **kwargs): 
        super(CompanyClientDiary, self).save( *args, **kwargs)     

class CompanyClientTest(Audit):
    client                      = models.ForeignKey(Client, verbose_name = _('Client*'))
    test                        = models.ForeignKey(Test, verbose_name = _('Test*')) 
    caregiver                   = models.ForeignKey(Caregiver, verbose_name = _('Caregiver*'))
    active                      = models.BooleanField(default = True, verbose_name = _('Active'))           
    assign_status               = models.BooleanField(default = True, verbose_name = _('Assign Status'))
    post_status                 = models.BooleanField(default = False, verbose_name = _('Post Status'))
    post_read_status            = models.BooleanField(default = False, verbose_name = _('Post Read Status'))
    
    def __unicode__(self):
        return str(self.test)

    class Meta:
        verbose_name            = _('ClientTest')
        verbose_name_plural     = _('ClientTests')
        
    def save(self, *args, **kwargs): 
        super(CompanyClientTest, self).save( *args, **kwargs)   

class ConfigurationContact(Audit):
    company                     = models.ForeignKey(Company, verbose_name = _('Company*'))
    name_of_institution         = models.CharField(max_length = 40, verbose_name = _('Name of Institution'), null = True, blank = True)
    email_external              = models.EmailField(verbose_name = _("E-Mail Address External Service Desk"), unique = True, null = True, blank = True)
    country_code_external       = models.PositiveIntegerField(max_length = 5, verbose_name = _("Country Code"), null = True, blank = True)
    phone_number_external       = models.CharField(max_length = 15, verbose_name = _('Telephone External Service Desk'), null = True, blank = True)
    email_internal              = models.EmailField(verbose_name = _("E-Mail Address Internal Service Desk"), unique = True, null = True, blank = True)    
    country_code_internal       = models.PositiveIntegerField(max_length = 5, verbose_name = _("Country Code"), null = True, blank = True)
    phone_number_internal       = models.CharField(max_length = 15, verbose_name = _('Telephone Internal Service Desk'), null = True, blank = True)
    
    def __unicode__(self):
        return self.company.company_name

    class Meta:
        verbose_name        = _('ConfigurationContact')
        verbose_name_plural = _('ConfigurationContacts')
        
    def save(self, *args, **kwargs): 
        super(ConfigurationContact, self).save( *args, **kwargs)    

class ConfigurationLogo(Audit):
    company             = models.ForeignKey(Company, verbose_name = _('Company*'))
    logo                = models.ImageField(upload_to = 'images/', null = True, blank = True, verbose_name = _('Logo'))
    favicon             = models.ImageField(upload_to = 'images/', null = True, blank = True, verbose_name = _('Favicon'))
    
    def __unicode__(self):
        return self.company.company_name

    class Meta:
        verbose_name        = _('ConfigurationLogo')
        verbose_name_plural = _('ConfigurationLogos')
        
    def save(self, *args, **kwargs): 
        super(ConfigurationLogo, self).save( *args, **kwargs)
        
class ConfigurationHomepage(Audit):
    company             = models.ForeignKey(Company, verbose_name = _('Company*'))
    header              = models.CharField(max_length = 50, null = True, blank = True, verbose_name = _('Header'))
    introduction        = models.TextField(max_length = 150, null = True, blank = True, verbose_name = _('Introduction'))
    
    def __unicode__(self):
        return self.company.company_name

    class Meta:
        verbose_name        = _('ConfigurationHomepage')
        verbose_name_plural = _('ConfigurationHomepages')
        
    def save(self, *args, **kwargs): 
        super(ConfigurationHomepage, self).save( *args, **kwargs)      
        
class ConfigurationLocation(Audit):
    company             = models.ForeignKey(Company, verbose_name = _('Company*'))
    country             = CountryField(null = True, blank = True, verbose_name = _('country'))
    continent           = models.CharField(max_length = 50, choices = continents, null = True, blank = True, verbose_name = _('Continent'))
    
    def __unicode__(self):
        return self.company.company_name

    class Meta:
        verbose_name        = _('ConfigurationHomepage')
        verbose_name_plural = _('ConfigurationHomepages')
        
    def save(self, *args, **kwargs): 
        super(ConfigurationLocation, self).save( *args, **kwargs)        
                     
class CompanyClientAssignment(Audit):
    client                      = models.ForeignKey(Client, verbose_name = _('Client*'))
    assignment                  = models.ForeignKey(Assignment, verbose_name = _('Assignment*')) 
    caregiver                   = models.ForeignKey(Caregiver, verbose_name = _('Caregiver*'))
    active                      = models.BooleanField(default = True, verbose_name = _('Active'))           
    assign_status               = models.BooleanField(default = True, verbose_name = _('Assign Status'))
    post_status                 = models.BooleanField(default = False, verbose_name = _('Post Status'))
    post_read_status            = models.BooleanField(default = False, verbose_name = _('Post Read Status'))
    
    def __unicode__(self):
        return self.assignment.name

    class Meta:
        verbose_name            = _('CompanyClientAssignment')
        verbose_name_plural     = _('CompanyClientAssignments')
        
    def save(self, *args, **kwargs): 
        super(CompanyClientAssignment, self).save( *args, **kwargs)
                  
class Messages(Audit):
    recipient                   = models.ForeignKey(User, verbose_name = _('Recipient*'))
    title                       = models.CharField(max_length = 40, verbose_name = _('Title*')) 
    description                 = models.TextField(max_length = 500, verbose_name = _('Description*'))
    attachment                  = models.FileField(max_length = 500, upload_to = _("messages"), null = True, blank = True, verbose_name = _('Attachment'))           
    read_status                 = models.BooleanField(default = False, verbose_name = _('Read Status'))
    delete_status               = models.BooleanField(default = False, verbose_name = _('Delete Status'))
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name            = _('Message')
        verbose_name_plural     = _('Messages')
        
    def save(self, *args, **kwargs): 
        super(Messages, self).save( *args, **kwargs)
                              
class SentMessages(Audit):
    recipient                   = models.ForeignKey(User, verbose_name = _('Recipient*'))
    title                       = models.CharField(max_length = 40, verbose_name = _('Title*')) 
    description                 = models.TextField(max_length = 500, verbose_name = _('Description*'))
    attachment                  = models.FileField(max_length = 500, upload_to = _("messages"), null = True, blank = True, verbose_name = _('Attachment'))           
   
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name            = _('Message')
        verbose_name_plural     = _('Messages')
        
    def save(self, *args, **kwargs): 
        super(SentMessages, self).save( *args, **kwargs)      
        
class CompanyClientAnimation(Audit):
    client                      = models.ForeignKey(Client, verbose_name = _('Client*'))
    caregiver                   = models.ForeignKey(Caregiver, verbose_name = _('Caregiver*'))
    animation                   = models.ForeignKey(Animation, verbose_name = _('Animation*'))
    active                      = models.BooleanField(default = True, verbose_name = _('Active'))
    assign_status               = models.BooleanField(default = True, verbose_name = _('Assign Status'))
    post_status                 = models.BooleanField(default = False, verbose_name = _('Post Status'))
    post_read_status            = models.BooleanField(default = False, verbose_name = _('Post Read Status'))
    
    def __unicode__(self):
        return u' %s' % (self.animation)

    class Meta:
        verbose_name            = _('Animation')
        verbose_name_plural     = _('Animations')
        
    def save(self, *args, **kwargs): 
        super(CompanyClientAnimation, self).save( *args, **kwargs)      
        
class CompanyForms(Audit):
    client                      = models.ForeignKey(Client, verbose_name = _('Client*'))
    form                        = models.CharField(max_length = 50, choices = form_names, verbose_name = _('Form*'))
    caregiver                   = models.ForeignKey(Caregiver, verbose_name = _('Caregiver*'))   
    assign_status               = models.BooleanField(default = True, verbose_name = _('Assign Status'))
    post_status                 = models.BooleanField(default = False, verbose_name = _('Post Status'))
    post_read_status            = models.BooleanField(default = False, verbose_name = _('Post Read Status'))
    
    def __unicode__(self):
        return self.form               
    
    def save(self, *args, **kwargs): 
        super(CompanyForms, self).save( *args, **kwargs)           