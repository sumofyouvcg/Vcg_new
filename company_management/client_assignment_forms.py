from django import forms
from django.utils.translation import ugettext as _

from vcg.company_management.models import CompanyClientAssignment 
from vcg.admin_management.models import Caregiver, Company, Assignment

class CompanyClientAssignmentForm(forms.ModelForm):
    class Meta:
        model = CompanyClientAssignment    

    def __init__(self, *args, **kw):

        user = kw.pop('user', None)
        caregiver_user = Caregiver.objects.filter(caregiver_number = user.username)
        company_user = Company.objects.filter(company_number = user.username)
        
        super(CompanyClientAssignmentForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = ""     
            
        if company_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = company_user[0].company_number, role__in = ['Company', 'Analyst'])
        elif caregiver_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = caregiver_user[0].company.company_number, role__in = ['Company', 'Analyst'])
        if not self.id:
            self.fields['assignment'].queryset = Assignment.objects.filter(active = True)
        
        self.fields['client'].widget.attrs['class']        = 'form-dropdownfield'
        self.fields['assignment'].widget.attrs['class']    = 'form-dropdownfield'
        self.fields['caregiver'].widget.attrs['class']     = 'form-dropdownfield'
        
    def clean(self):
        client       = self.cleaned_data.get("client")
        assignment    = self.cleaned_data.get("assignment")
        
        qs = CompanyClientAssignment.objects.filter(client = client, assignment = assignment)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Assignment  already Exists.'))    
        return self.cleaned_data  