from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from vcg.company_management.models import CompanyClientDiary 
from vcg.admin_management.models import Caregiver, Company, Diary

class CompanyClientDiaryForm(forms.ModelForm):
    class Meta:
        model = CompanyClientDiary    

    def __init__(self, *args, **kw):

        user = kw.pop('user', None)
        caregiver_user = Caregiver.objects.filter(caregiver_number = user.username)
        company_user = Company.objects.filter(company_number = user.username)
        
        super(CompanyClientDiaryForm, self).__init__(*args, **kw)
        
        if company_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = company_user[0].company_number, role__in = ['Company', 'Analyst'])
        elif caregiver_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = caregiver_user[0].company.company_number, role__in = ['Company', 'Analyst'])

        self.fields['client'].widget.attrs['class']        = 'form-dropdownfield'
        self.fields['diary'].widget.attrs['class']         = 'form-dropdownfield'
        self.fields['caregiver'].widget.attrs['class']     = 'form-dropdownfield'
        self.fields['intervel'].widget.attrs['class']      = 'form-dropdownfield'
        
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 
        
        if not self.id:
            self.fields['diary'].queryset = Diary.objects.filter(active = True)
         
    def user_unicode(self):
        return self.name + ' (' + str(self.caregiver_number) + ')'
    Caregiver.__unicode__ = user_unicode    
        
    
    def clean(self):
        client   = self.cleaned_data.get("client")
        diary    = self.cleaned_data.get("diary")
        
        qs = CompanyClientDiary.objects.filter(client = client, diary = diary)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Diary  already Exists for this Client.'))    
        return self.cleaned_data  