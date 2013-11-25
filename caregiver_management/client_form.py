import datetime, calendar
from django import forms
from django.forms import fields
from django.utils.translation import ugettext as _

from vcg.config.choices import caregiver_choices, diary_choices, company, treatment_module, treatment_guidence, treatment_sessions, motivation_plans, practise_plans

class ClientMessageForm(forms.Form):
    title                     = fields.CharField(required = True)
    description               = fields.CharField(widget = forms.Textarea, required = True)
    attachment                = fields.FileField(required = False)
    

class ClientDiaryAddForm(forms.Form):
    diary                     = fields.ChoiceField(choices = diary_choices, required = False)
    caregiver                 = fields.ChoiceField(choices = caregiver_choices, required = False)

    def clean_diary(self):
        diary = self.cleaned_data['diary']
        if diary == '0':
            raise forms.ValidationError(_('This field is required.'))
        return diary  

    def clean_caregiver(self):
        caregiver = self.cleaned_data['caregiver']
        if caregiver == '0':
            raise forms.ValidationError(_('This field is required.'))
        return caregiver

class ClientTreatmentAddForm(forms.Form):
    treatment_module           = fields.ChoiceField(choices = treatment_module, required = False)
    title                      = fields.CharField(required = True)
    company                    = fields.ChoiceField(choices = company, required = False)
    first_session_activation   = fields.BooleanField(required = True)        
    guidence                   = fields.ChoiceField(choices = treatment_guidence, required = False)

    def clean_treatment_module(self):
        treatment_module = self.cleaned_data['treatment_module']
        if treatment_module == '0':
            raise forms.ValidationError(_('This field is required.'))
        return treatment_module

    def clean_company(self):
        company = self.cleaned_data['company']
        if company == '0':
            raise forms.ValidationError(_('This field is required.'))
        return company  

    def clean_guidence(self):
        guidence = self.cleaned_data['guidence']
        if guidence == '0':
            raise forms.ValidationError(_('This field is required.'))
        return guidence
          
class ClientTreatmentCustomForm(forms.Form):    
    treatment_module           = fields.ChoiceField(choices = treatment_module, required = False)
    sessions                   = fields.ChoiceField(choices = treatment_sessions, required = False)

    def clean_treatment_module(self):
        treatment_module = self.cleaned_data['treatment_module']
        if treatment_module == '0':
            raise forms.ValidationError(_('This field is required.'))
        return treatment_module

    def clean_sessions(self):
        sessions = self.cleaned_data['sessions']
        if sessions == '0':
            raise forms.ValidationError(_('This field is required.'))
        return sessions  
        
class ClientMplanAddForm(forms.Form):    
    motivation_plan = fields.ChoiceField(choices = motivation_plans, required = False)
    goal            = fields.CharField(required = True)
    description     = fields.CharField(widget = forms.Textarea, required = True)
    goal_achived    = fields.CharField(required = True)                                                  

    def clean_motivation_plan(self):
        motivation_plan = self.cleaned_data['motivation_plan']
        if motivation_plan == '0':
            raise forms.ValidationError(_('This field is required.'))
        return motivation_plan
    
class ClientPlanAddForm(forms.Form):    
    plan         = fields.ChoiceField(choices = practise_plans, required = False)
    goal         = fields.CharField(required = True)
    description  = fields.CharField(widget = forms.Textarea, required = True)
    goal_achived = fields.CharField(required = True)                                                  
