from django import forms
from django.utils.translation import ugettext as _

from vcg.company_management.models import CompanyClientTest
from vcg.admin_management.models import TestModule, Caregiver, Company, Test

class CompanyClientTestForm(forms.ModelForm):
    class Meta:
        model = CompanyClientTest    

    def __init__(self,  *args, **kw):
        user = kw.pop('user', None)
        
        caregiver = Caregiver.objects.filter(caregiver_number = user.username)
        company = Company.objects.filter(company_number = user.username)
        
        super(CompanyClientTestForm, self).__init__(*args, **kw)
        
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 
        
        test_list = []    
        if company:
            company_test = TestModule.objects.filter(company__company_number = company[0].company_number)    
            for test in company_test:
                test_list.append(test.tests.id)
           
            if not self.id:
                self.fields['test'].queryset = Test.objects.filter(id__in = test_list, active =True)
            else:
                self.fields['test'].queryset = Test.objects.filter()
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = company[0].company_number, role__in = ['Company', 'Analyst'])

        elif caregiver:
            company_test = TestModule.objects.filter(company__company_number = caregiver[0].company.company_number)    
            for test in company_test:
                test_list.append(test.tests.id)

            if not self.id:
                self.fields['test'].queryset = Test.objects.filter(id__in = test_list, active =True)
            else:
                self.fields['test'].queryset = Test.objects.filter()
            self.fields['caregiver'].queryset = Caregiver.objects.filter(company__company_number = caregiver[0].company.company_number, role__in = ['Company', 'Analyst'])

         
        self.fields['client'].widget.attrs['class']        = 'form-dropdownfield'
        self.fields['test'].widget.attrs['class']          = 'form-dropdownfield'
        self.fields['caregiver'].widget.attrs['class']     = 'form-dropdownfield'
        
        
    def clean(self):
        client       = self.cleaned_data.get("client")
        test         = self.cleaned_data.get("test")
        
        qs = CompanyClientTest.objects.filter(client = client, test = test)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Test  already Exists for this Client.'))    
        return self.cleaned_data
    