import re

from django import forms
from django.forms import fields
from django.utils.translation import ugettext as _

from vcg.company_management.models import CompanyClientTreatment, ClientTreatmentSessions, ClientSessionsFeedback
#from vcg.config.choices import treatment_sessions, treatment_module
from vcg.admin_management.models import Caregiver, CompanyModules, Company, Module

class CompanyClientTreatmentForm(forms.ModelForm):
    class Meta:
        model = CompanyClientTreatment
        
    def __init__(self, *args, **kw):
        
        user = kw.pop('user', None)
        caregiver_user = Caregiver.objects.filter(caregiver_number = user.username)
        company_user = Company.objects.filter(company_number = user.username)
        super(CompanyClientTreatmentForm, self).__init__(*args, **kw)
        
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 
            
        module_list = []    
        if company_user:
            company_modules = CompanyModules.objects.filter(company__company_number = company_user[0].company_number)    
            for modules in company_modules:
                module_list.append(modules.modules.id)
           
            if not self.id:
                self.fields['module'].queryset = Module.objects.filter(id__in = module_list, active =True)
            else:
                self.fields['module'].queryset = Module.objects.filter()
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = company_user[0].company_number, role__in = ['Company', 'Analyst'])

        elif caregiver_user:
            company_modules = CompanyModules.objects.filter(company__company_number = caregiver_user[0].company.company_number)    
            for modules in company_modules:
                module_list.append(modules.modules.id)

            if not self.id:
                self.fields['module'].queryset = Module.objects.filter(id__in = module_list, active =True)
            else:
                self.fields['module'].queryset = Module.objects.filter()
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = caregiver_user[0].company.company_number, role__in = ['Company', 'Analyst'])
    
        self.fields['title'].widget.attrs['class']       = 'form-text'
        self.fields['guidance'].widget.attrs['class']    = 'form-dropdownfield'
        self.fields['caregiver'].widget.attrs['class']   = 'form-dropdownfield'
        self.fields['module'].widget.attrs['class'] = 'form-dropdownfield'
        
    def clean(self):
        client              = self.cleaned_data.get("client")
        treatment_module    = self.cleaned_data.get("module")
        
        qs = CompanyClientTreatment.objects.filter(client = client, module = treatment_module)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Treatment Module  already Exists for this Client.'))    
        return self.cleaned_data 
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'^[\s]*$', title):
            raise forms.ValidationError(_('Enter a valid Title.'))
        elif len(title) < 5:
            raise forms.ValidationError(_('Enter minimum 5 characters.'))
        elif not re.match(r'^[\sA-Za-z]+(?:[\s-][A-Za-z\s]+)*$', title):
            raise forms.ValidationError(_('Alphabet characters only.'))
        return title
    
    def clean_treatment_module(self):
        treatment_module = self.cleaned_data['treatment_module']
        if treatment_module == '0':
            raise forms.ValidationError(_('This field is required.'))
        return treatment_module

    def clean_caregiver(self):
        caregiver = self.cleaned_data['caregiver']
        if caregiver == '0':
            raise forms.ValidationError(_('This field is required.'))
        return caregiver  

    def clean_guidance(self):
        guidence = self.cleaned_data['guidance']
        if guidence == '0':
            raise forms.ValidationError(_('This field is required.'))
        return guidence
    
class ClientTreatmentCustomForm(forms.Form):    
    treatment_module           = fields.ChoiceField(required = False)
    sessions                   = fields.ChoiceField(required = False)

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
    
class ClientTreatmentSessionsForm(forms.ModelForm):
    class Meta:
        model = ClientTreatmentSessions
        
    def __init__(self, *args, **kw):
        user = kw.pop('user', None)
        caregiver_user = Caregiver.objects.filter(caregiver_number = user.username)
        company_user = Company.objects.filter(company_number = user.username)
        super(ClientTreatmentSessionsForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 
            
        module_list = []    
        if company_user:
            company_modules = CompanyModules.objects.filter(company__company_number = company_user[0].company_number)    
            for modules in company_modules:
                module_list.append(modules.modules.id)
           
            if not self.id:
                self.fields['module'].queryset = Module.objects.filter(id__in = module_list, active =True)
            else:
                self.fields['module'].queryset = Module.objects.filter()
            
        elif caregiver_user:
            company_modules = CompanyModules.objects.filter(company__company_number = caregiver_user[0].company.company_number)    
            for modules in company_modules:
                module_list.append(modules.modules.id)

            if not self.id:
                self.fields['module'].queryset = Module.objects.filter(id__in = module_list, active =True)
            else:
                self.fields['module'].queryset = Module.objects.filter()
            
            
        self.fields['sessions'].widget.attrs['class'] = 'form-dropdownfield'
        self.fields['module'].widget.attrs['class']   = 'form-dropdownfield'
        
    def clean_module(self):
        treatment_module = self.cleaned_data['module']
        if treatment_module == '0':
            raise forms.ValidationError(_('This field is required.'))
        return treatment_module

    def clean_sessions(self):
        sessions = self.cleaned_data['sessions']
        if sessions == '0':
            raise forms.ValidationError(_('This field is required.'))
        return sessions  
       
class ClientSessionsFeedbackForm(forms.ModelForm):
    class Meta:
        model = ClientSessionsFeedback
        
    def __init__(self, *args, **kw):
        super(ClientSessionsFeedbackForm, self).__init__(*args, **kw)
        
        self.fields['feedback'].widget.attrs['class']       = 'form-textarea-feed'
        self.fields['feedback'].widget.attrs['maxlength']   = '150'
        
    def clean_feedback(self):
        feedback = self.cleaned_data['feedback']
        if len(feedback) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', feedback):
            raise forms.ValidationError(_("Enter a valid feedback."))
        return feedback 