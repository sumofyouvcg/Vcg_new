from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from vcg.company_management.models import CompanyForms 
from vcg.admin_management.models import Caregiver, Company, Diary

class CompanyFormsForm(forms.ModelForm):
    class Meta:
        model = CompanyForms    

    def __init__(self, *args, **kw):

        user = kw.pop('user', None)
        caregiver_user = Caregiver.objects.filter(caregiver_number = user.username)
        company_user = Company.objects.filter(company_number = user.username)
        
        super(CompanyFormsForm, self).__init__(*args, **kw)
        
        if company_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = company_user[0].company_number, role__in = ['Company', 'Analyst'])
        elif caregiver_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = caregiver_user[0].company.company_number, role__in = ['Company', 'Analyst'])

        self.fields['client'].widget.attrs['class']        = 'form-dropdownfield'
        self.fields['form'].widget.attrs['class']         = 'form-dropdownfield'
        self.fields['caregiver'].widget.attrs['class']     = 'form-dropdownfield'
        
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 
        
         
    def user_unicode(self):
        return self.name + ' (' + str(self.caregiver_number) + ')'
    Caregiver.__unicode__ = user_unicode    
        
    
    def clean(self):
        client   = self.cleaned_data.get("client")
        form    = self.cleaned_data.get("form")
        
        qs = CompanyForms.objects.filter(client = client, form = form)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Form already Exists for this Client.'))    
        return self.cleaned_data  
    
    def clean_form(self):
        form = self.cleaned_data['form']
        print form
        if form == '0':
            raise forms.ValidationError(_('This field is required.'))
        return form   