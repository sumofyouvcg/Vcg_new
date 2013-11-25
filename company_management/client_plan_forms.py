import re
from django import forms
from django.utils.translation import ugettext as _

from vcg.company_management.models import CompanyClientPlan
from vcg.admin_management.models import Caregiver, Company, Plan

class CompanyClientPlanForm(forms.ModelForm):
    class Meta:
        model = CompanyClientPlan    

    def __init__(self, *args, **kw):

        user = kw.pop('user', None)
        caregiver_user = Caregiver.objects.filter(caregiver_number = user.username)
        company_user = Company.objects.filter(company_number = user.username)
        
        super(CompanyClientPlanForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 
                    
        if company_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = company_user[0].company_number, role__in = ['Company', 'Analyst'])
        elif caregiver_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = caregiver_user[0].company.company_number, role__in = ['Company', 'Analyst'])
        if not self.id:
            self.fields['practise_plan'].queryset = Plan.objects.filter(active =True)                                                        

        self.fields['client'].widget.attrs['class']                 = 'form-dropdownfield'
        self.fields['caregiver'].widget.attrs['class']              = 'form-dropdownfield'
        self.fields['practise_plan'].widget.attrs['class']          = 'form-dropdownfield'
        self.fields['goal'].widget.attrs['class']                   = 'form-text'
        self.fields['goal_achieved'].widget.attrs['class']          = 'form-text'



    def clean(self):
        client       = self.cleaned_data.get("client")
        practise_plan    = self.cleaned_data.get("practise_plan")
        
        qs = CompanyClientPlan.objects.filter(client = client, practise_plan = practise_plan)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Practise Plan  already Exists for this Client.'))    
        return self.cleaned_data 
    
    def clean_goal(self):
        goal = self.cleaned_data['goal']
        if len(goal) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', goal):
            raise forms.ValidationError(_("Enter a valid name."))
        return goal 
    
    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 10:
            raise forms.ValidationError(_('Enter minimum 10 characters.'))
        elif  re.match(r'^[\s]*$', description):
            raise forms.ValidationError(_("Enter a valid address."))
        return description

    def clean_goal_achieved(self):
        goal_achieved = self.cleaned_data['goal_achieved']
        if len(goal_achieved) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', goal_achieved):
            raise forms.ValidationError(_("Enter a valid name."))
        return goal_achieved        