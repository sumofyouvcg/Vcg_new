from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from vcg.ckeditor.fields import RichTextField
from django_countries import CountryField
from vcg.config.choices import roles, answer_type, gender
from vcg.util.models import Audit

class Company(Audit):
    company_name        = models.CharField(max_length = 40, verbose_name = _('Company Name*'))
    company_number      = models.CharField(unique = True, max_length = 20, verbose_name = _('Company Number*'))
    address             = models.TextField(max_length = 150, verbose_name = _('Address*'))
    zip_code            = models.CharField(max_length = 10, verbose_name = _('ZIP Code*'))
    place_name          = models.CharField(max_length = 150, verbose_name = _('Place Name*'))
    country             = CountryField(null = True, blank = True, verbose_name = _('Country*'))
    email               = models.EmailField(verbose_name = _("E-Mail*"), unique = True)
    country_code        = models.PositiveIntegerField(max_length = 5, verbose_name = _("Country Code*"))
    phone_number        = models.CharField(max_length = 15, verbose_name = _('Contact Number*'))
    number_of_clients   = models.PositiveIntegerField(verbose_name = _('Number of Clients*'))
    from_date           = models.DateField(verbose_name = _('From Date*'))
    expiry_date         = models.DateField(verbose_name = _('Expiry Date*'))
    sub_domain          = models.CharField(unique = True, max_length = 15, verbose_name = _('Sub Domain*'))
    language            = models.CharField(max_length = 10, verbose_name = _('Language'))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.company_name

    class Meta:
        verbose_name        = _('Company')
        verbose_name_plural = _('Companies')
        
    def save(self, *args, **kwargs): 
        super(Company, self).save( *args, **kwargs)

class Caregiver(Audit):
    name                = models.CharField(max_length = 50, verbose_name = _('Name*'))
    sur_name            = models.CharField(max_length = 50, verbose_name = _('Sur Name'), null = True, blank = True)
    last_name           = models.CharField(max_length = 50, verbose_name = _('Last Name*'))
    address             = models.TextField(max_length = 150, verbose_name = _('Address*'))
    zip_code            = models.CharField(max_length = 10, verbose_name = _('ZIP Code*'))
    place_name          = models.CharField(max_length = 150, verbose_name = _('Place Name*'))
    country             = CountryField(null = True, blank = True, verbose_name = _('Country*'))
    email               = models.EmailField(verbose_name = _("E-Mail*"))
    dob                 = models.DateField(verbose_name = _('Date of Birth*'))
    gender              = models.CharField(max_length = 50, choices = gender, verbose_name = _('Gender*'))
    country_code        = models.PositiveIntegerField(verbose_name = _("Country Code*"))
    phone_number        = models.CharField(max_length = 15, verbose_name = _('Contact Number*'))    
    company             = models.ForeignKey(Company, verbose_name = _('Company*'))
    role                = models.CharField(max_length = 50, choices = roles, verbose_name = _('Role*'))
    caregiver_number    = models.CharField(unique = True, max_length = 20, verbose_name = _('Caregiver Number*'))
    caregiver_image     = models.ImageField(max_length = 500, upload_to = 'images/', verbose_name = _('Photo'), null = True, blank = True, help_text=_("Accepts .jpeg,jpg,png files only"))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name        = _('Caregiver')
        verbose_name_plural = _('Caregivers')

class Client(Audit):
    name                = models.CharField(max_length = 50, verbose_name = _('Name*'))
    sur_name            = models.CharField(max_length = 50, verbose_name = _('Sur Name'), null = True, blank = True)
    last_name           = models.CharField(max_length = 50, verbose_name = _('Last Name*'))
    address             = models.TextField(max_length = 150, verbose_name = _('Address*'))
    zip_code            = models.CharField(max_length = 10, verbose_name = _('ZIP Code*'))
    place_name          = models.CharField(max_length = 150, verbose_name = _('Place Name*'))
    country             = CountryField(null = True, blank = True, verbose_name = _('Country*'))
    email               = models.EmailField(verbose_name = _("E-Mail*"))
    country_code        = models.PositiveIntegerField(verbose_name = _("Country Code*"))
    phone_number        = models.CharField(max_length = 15, verbose_name = _('Contact Number*'))    
    bsn_number          = models.CharField(max_length = 15, verbose_name = _('BSN Number*'))
    dob                 = models.DateField(verbose_name = _('Date of Birth*'))
    age                 = models.PositiveIntegerField(max_length = 3, verbose_name = _('Age*'))
    gender              = models.CharField(max_length = 50, choices = gender, verbose_name = _('Gender*'))
    client_number       = models.CharField(unique = True, max_length = 20, verbose_name = _('Client Number*'))
    insurance_name      = models.CharField(max_length = 40, verbose_name = _('Insurance Name'), null = True, blank = True)
    insurance_number    = models.CharField(max_length = 40, verbose_name = _('Insurance Number'), null = True, blank = True)
    company             = models.ForeignKey(Company, verbose_name = _('Company*'))
    client_image        = models.ImageField(max_length = 500, upload_to = 'images/', verbose_name = _('Photo'), null = True, blank = True, help_text=_("Accepts .jpeg,jpg,png files only"))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name        = _('Client')
        verbose_name_plural = _('Clients')
        
class Plan(Audit):
    title               = models.CharField(max_length = 50, verbose_name = _('Title*'))
    description         = models.TextField(max_length = 500, verbose_name = _('Description*'))
    image               = models.ImageField(max_length = 500, upload_to = 'images/', verbose_name = _('Image*'), help_text = _("Accepts .jpeg,jpg,png files only"))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name        = _('Plan')
        verbose_name_plural = _('Plans')
        
class Diary(Audit):
    title               = models.CharField(max_length = 50, verbose_name = _('Title*'))
    diary_number        = models.CharField(unique = True, max_length = 40, verbose_name = _('Diary Number*'))
    image               = models.ImageField(max_length = 500, verbose_name = _('Image*'), upload_to = 'images/', help_text=_("Accepts .jpeg,jpg,png files only"))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name        = _('Diary')
        verbose_name_plural = _('Diaries')

class DiaryQuestion(Audit):
    diary               = models.ForeignKey(Diary, null = True, blank = True, verbose_name = _('Diary'))
    question            = models.CharField(max_length = 150, verbose_name = _('Question*'))
    help_text           = models.CharField(max_length = 150, verbose_name = _('Help Text*'))
    answer_type         = models.CharField(max_length = 150, default = '0', choices = answer_type, verbose_name = _('Answer Type*'))
    
    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name        = _('DiaryQuestion')
        verbose_name_plural = _('DiaryQuestions')
                
class QuestionChoice(Audit):
    diary_question      = models.ForeignKey(DiaryQuestion, null = True, blank = True, verbose_name = _('Diary Question'))
    answer              = models.TextField(max_length = 150, help_text = _("Enter the Answer one per Line"), verbose_name = _('Answer*'))

    def __unicode__(self):
        return self.answer

    class Meta:
        verbose_name        = _('QuestionChoice')
        verbose_name_plural = _('QuestionChoices')
        
class QuestionSlider(Audit):
    diary_question      = models.ForeignKey(DiaryQuestion, null = True, blank = True, verbose_name = _('Diary Question'))
    min_value           = models.PositiveIntegerField(max_length = 10, verbose_name = _('Min Value*'))
    max_value           = models.PositiveIntegerField(max_length = 10, verbose_name = _('Max Value*'))
    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name        = _('QuestionChoice')
        verbose_name_plural = _('QuestionChoices')
        
class Animation(Audit):
    name                = models.CharField(max_length = 50, unique = True, verbose_name = _('Name*'))
    location            = models.FileField(_('Animation*'), upload_to = "animations")
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name        = _('Animation')
        verbose_name_plural = _('Animations')
        
    def save(self, *args, **kwargs): 
        super(Animation, self).save( *args, **kwargs)
        
class Module(Audit):
    name                = models.CharField(unique = True, max_length = 40, verbose_name = _("Module Name*"))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name        = _('Module')
        verbose_name_plural = _('Modules')
        
    def save(self, *args, **kwargs): 
        super(Module, self).save( *args, **kwargs)
        
class Session(Audit):
    name            = models.CharField(max_length = 40, verbose_name = _('Name*'))
    module          = models.ForeignKey(Module, verbose_name = _('Module*'))
    plaintext       = RichTextField(blank = True, null = True, verbose_name = _('Plain text'))
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name        = _('Session')
        verbose_name_plural = _('Sessions')
        
    def save(self, *args, **kwargs): 
        super(Session, self).save( *args, **kwargs)
        
class ModuleAnimation(Audit):
    module              = models.ForeignKey(Module, verbose_name = _('Module'))
    animation           = models.ForeignKey(Animation, verbose_name = _('Animation'))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.module.name

    class Meta:
        verbose_name        = _('ModuleAnimation')
        verbose_name_plural = _('ModuleAnimations')
        
    def save(self, *args, **kwargs): 
        super(ModuleAnimation, self).save( *args, **kwargs)
        
class CreateQuestion(Audit):
    module              = models.ForeignKey(Module, verbose_name = _('Module*'))
    question_text       = models.CharField(max_length = 100, verbose_name = _('Question Text*'))
    help_text           = models.CharField(max_length = 50, verbose_name = _('Help Text*'))
    answer_type         = models.CharField(max_length = 20, default = '0', choices = answer_type, verbose_name = _('Answer Type*'))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.question_text

    class Meta:
        verbose_name        = _('Create Question')
        verbose_name_plural = _('Create Questions')
        
    def save(self, *args, **kwargs): 
        super(CreateQuestion, self).save( *args, **kwargs)

class CreateQuestionChoice(Audit):
    create_question     = models.ForeignKey(CreateQuestion, null = True, blank = True, verbose_name = _('Create Question'))
    answer              = models.TextField(max_length = 500, verbose_name = _('Answer*'), help_text = _("Enter the Answer one per Line"))

    def __unicode__(self):
        return self.answer

    class Meta:
        verbose_name        = _('QuestionChoice')
        verbose_name_plural = _('QuestionChoices')
        
class CreateQuestionSlider(Audit):
    create_question     = models.ForeignKey(CreateQuestion, null = True, blank = True, verbose_name = _('Create Question'))
    min_value           = models.PositiveIntegerField(max_length = 10, verbose_name = _('Min Value*'))
    max_value           = models.PositiveIntegerField(max_length = 10, verbose_name = _('Max Value*'))

    def __unicode__(self):
        return self.create_question.question_text

    class Meta:
        verbose_name        = _('CreateQuestionSlider')
        verbose_name_plural = _('CreateQuestionSliders') 
             
class Assignment(Audit):
    name                = models.CharField(max_length = 100, unique = True, verbose_name = _('Name*'))
    summary             = models.TextField(verbose_name = _('Summary*'))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name        = _('Assignment')
        verbose_name_plural = _('Assignments')
        
    def save(self, *args, **kwargs): 
        super(Assignment, self).save(*args, **kwargs)
        
class AssignmentCluster(Audit):
    assignment          = models.ForeignKey(Assignment, verbose_name = _('Assignment'))
    cluster_name        = models.CharField(max_length = 100, verbose_name = _('Cluster Name*'))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.cluster_name

    class Meta:
        verbose_name        = _('AssignmentCluster')
        verbose_name_plural = _('AssignmentClusters')
        
    def save(self, *args, **kwargs): 
        super(AssignmentCluster, self).save( *args, **kwargs)
        
class AssignmentQuestion(Audit):
    assignment_cluster  = models.ForeignKey(AssignmentCluster, verbose_name = _('Assignment Cluster*'))
    question_text       = models.CharField(max_length = 500, verbose_name = _('Question Text*'))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.question_text

    class Meta:
        verbose_name        = _('AssignmentQuestion')
        verbose_name_plural = _('AssignmentQuestions')
        
    def save(self, *args, **kwargs): 
        super(AssignmentQuestion, self).save(*args, **kwargs)
        
class AssignmentQuestionAnswer(Audit):
    assignment_question = models.ForeignKey(AssignmentQuestion, blank= True, null = True, verbose_name = _('Assignment Question'))
    option              = models.CharField(max_length = 100, verbose_name = _('Option'))
    answer              = models.BooleanField(default = False, verbose_name = _('Answer'))
    active              = models.BooleanField(default = True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return self.option

    class Meta:
        verbose_name        = _('AssignmentQuestionAnswer')
        verbose_name_plural = _('AssignmentQuestionAnswers')
        
    def save(self, *args, **kwargs): 
        super(AssignmentQuestionAnswer, self).save(*args, **kwargs)
        
class CompanyModules(Audit):
    company             = models.ForeignKey(Company, verbose_name = _('Company'))
    modules             = models.ForeignKey(Module, verbose_name = _('Module'))
    
    def __unicode__(self):
        return self.modules.name

    class Meta:
        verbose_name        = _('CompanyModules')
        verbose_name_plural = _('CompanyModules')
        
    def save(self, *args, **kwargs): 
        super(CompanyModules, self).save(*args, **kwargs)

class Test(Audit):
    title  = models.CharField(_('Title'), max_length = 50, unique = True)
    active = models.BooleanField(_('Active'), default = True)

    def __unicode__(self):
        return self.title

class TestQuestion(Audit):
    test     = models.ForeignKey(Test, verbose_name = _('Test'))
    question = models.CharField(_('Question*'), max_length = 150)

    def __unicode__(self):
        return self.question

class TestQuestionAnswers(Audit):
    question = models.ForeignKey(TestQuestion, verbose_name = _('Test Question'))
    answer   = models.CharField(_('Question*'), max_length = 150)
    score    = models.CharField(_('Score*'), max_length = 5)

    def __unicode__(self):
        return self.answer

class TestRange(Audit):
    test       = models.ForeignKey(Test, verbose_name = _('Test'))
    from_value = models.PositiveIntegerField(verbose_name = _('From Value'))
    to_value   = models.PositiveIntegerField(verbose_name = _('To Value'))
    result     = models.CharField(max_length = 150, verbose_name = _('Result'))

    def  __unicode__(self):
        return self.result

class TestModule(Audit):
    company             = models.ForeignKey(Company, verbose_name = _('Company'))
    tests               = models.ForeignKey(Test, verbose_name = _('Test'))
    
    def __unicode__(self):
        return self.tests.title

class AdminUser(Audit):
    first_name        = models.CharField(max_length = 50, verbose_name = _('First Name*'))
    last_name         = models.CharField(max_length = 50, verbose_name = _('Last Name*'))
    email             = models.EmailField(unique = True, verbose_name = _("E-Mail*"))
    active            = models.BooleanField(default = True, verbose_name = _('Active'))
    user_id           = models.CharField(max_length = 50, unique = True, verbose_name = _("User-ID*"))
        
    def __unicode__(self):
        return self.first_name

    class Meta:
        verbose_name        = _('AdminUser')
        verbose_name_plural = _('AdminUsers')
        
class AdminUserPermission(Audit):
    admin_user        = models.ForeignKey(AdminUser, verbose_name = _('AdminUser'))
    create_file       = models.CharField(max_length = 550, blank = True, null = True)
          
    def __unicode__(self):
        return self.admin_user.first_name

    class Meta:
        verbose_name        = _('AdminUserPermission')
        verbose_name_plural = _('AdminUserPermissions')

class MailConfiguration(Audit):
    english        = models.TextField(max_length = 500, blank = True, null = True, verbose_name = _('English'))
    dutch          = models.TextField(max_length = 500, blank = True, null = True, verbose_name = _('Dutch'))
          
    def __unicode__(self):
        return self.english

    class Meta:
        verbose_name        = _('MailConfiguration')
        verbose_name_plural = _('MailConfigurations')

class VideoSession(models.Model):
    sender     = models.ForeignKey(User, related_name = 'sender_user1')
    receiver   = models.ForeignKey(User, related_name = 'receiver_user1')
    session_id = models.CharField(max_length = 255)
    token_id   = models.TextField()

