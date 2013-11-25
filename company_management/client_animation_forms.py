import re
from django import forms
from django.utils.translation import ugettext as _

from vcg.company_management.models import CompanyClientAnimation
from vcg.admin_management.models import Caregiver, Company, Animation

class CompanyClientAnimationForm(forms.ModelForm):
    class Meta:
        model = CompanyClientAnimation    

    def __init__(self, *args, **kw):

        user = kw.pop('user', None)
        caregiver_user = Caregiver.objects.filter(caregiver_number = user.username)
        company_user   = Company.objects.filter(company_number = user.username)
        
        super(CompanyClientAnimationForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 
                    
        if company_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = company_user[0].company_number)
        elif caregiver_user:
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = caregiver_user[0].company.company_number)
        if not self.id:
            self.fields['animation'].queryset = Animation.objects.filter(active =True)                                                        

        self.fields['client'].widget.attrs['class']                 = 'form-dropdownfield'
        self.fields['caregiver'].widget.attrs['class']              = 'form-dropdownfield'
        self.fields['animation'].widget.attrs['class']              = 'form-dropdownfield'

    def clean(self):
        client       = self.cleaned_data.get("client")
        animation    = self.cleaned_data.get("animation")
        
        qs = CompanyClientAnimation.objects.filter(client = client, animation = animation)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Animation already Exists for this Client.'))    
        return self.cleaned_data
