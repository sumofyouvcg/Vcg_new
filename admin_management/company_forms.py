import re
import datetime

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from vcg.util.forms import HorizontalRadioRenderer
from vcg.admin_management.models import Company, AdminUser, Caregiver, Client
from vcg.util.forms import mobile_number_validation

LANGUAGES = (('English', 'English',), ('Dutch', 'Dutch',))

class CompanyForm(forms.ModelForm):
    language = forms.ChoiceField(initial=0, widget = forms.RadioSelect(renderer = HorizontalRadioRenderer), choices=LANGUAGES)
    class Meta:
        model = Company
        
    def __init__(self, *args, **kw):
        super(CompanyForm, self).__init__(*args, **kw)
        self.fields['company_name'].widget.attrs['class']       = 'form-text'
        self.fields['address'].widget.attrs['class']            = 'form-textarea'
        self.fields['zip_code'].widget.attrs['class']           = 'form-text'
        self.fields['place_name'].widget.attrs['class']         = 'form-text'
        self.fields['country'].widget.attrs['class']            = 'form-dropdownfield'
        self.fields['email'].widget.attrs['class']              = 'form-text'
        self.fields['country_code'].widget.attrs['class']       = 'form-text-small'
        self.fields['phone_number'].widget.attrs['class']       = 'form-text-phone'
        self.fields['number_of_clients'].widget.attrs['class']  = 'form-text'
        self.fields['sub_domain'].widget.attrs['class']         = 'form-text'
        self.fields['company_number'].widget.attrs['class']     = 'form-text'
        self.fields['from_date'].widget.attrs['class']          = 'datepicker_from'
        self.fields['expiry_date'].widget.attrs['class']        = 'datepicker_to'
        
        self.fields['address'].widget.attrs['maxlength']        = '150'
        
        if 'instance' in kw:
            self.id = kw['instance'].id
            self.company_number = kw['instance'].company_number
        else:
            self.id = ""     
            self.company_number = "" 

    def clean(self):
        email      = self.cleaned_data.get("email")
        sub_domain = self.cleaned_data.get("sub_domain")

        caregiver  = Caregiver.objects.filter(company__sub_domain = sub_domain, email = email)
        client     = Client.objects.filter(company__sub_domain = sub_domain, email = email)
        admin_user = AdminUser.objects.filter(email = email)
        if admin_user:
            raise forms.ValidationError(_('Email Already Exists.'))
        if caregiver or client:
            raise forms.ValidationError(_('Email Already Exists.'))
        return self.cleaned_data    
          
    def clean_email(self):
        email      = self.cleaned_data['email']
        qs = Company.objects.filter(email = email)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('Email Already Exits.'))
        return email
    
    def clean_company_name(self):
        name = self.cleaned_data['company_name']
        if len(name) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', name):
            raise forms.ValidationError(_("Enter a valid name."))
        return name 
    
    def clean_address(self):
        address = self.cleaned_data['address']
        if len(address) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        elif  re.match(r'^[\s]*$', address):
            raise forms.ValidationError(_("Enter a valid address."))
        return address 

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if len(zip_code) < 5:
            raise forms.ValidationError(_('Enter minimum 4 characters.'))
        elif  re.match(r'^[\s]*$', zip_code):
            raise forms.ValidationError(_("Enter a valid Zip Code."))
        if not re.match(r'^[\sA-Za-z,0-9]+(?:[\s-][A-Za-z\s]+)*$', zip_code):
            raise forms.ValidationError(_('Alphabets and Numbers Only.'))
        return zip_code 
        
    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob != None:
            if dob > datetime.date.today():
                raise forms.ValidationError(_("Date cannot be in future"))
            return dob
        
    def clean_place_name(self):
        place_name = self.cleaned_data['place_name']
        if len(place_name) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', place_name):
            raise forms.ValidationError(_("Enter a valid Place Name."))
        if not re.match(r'^[\sA-Za-z,0-9]+(?:[\s-][A-Za-z\s]+)*$', place_name):
            raise forms.ValidationError(_('Alphabets and Numbers Only.'))
        return place_name 

    def clean_country(self):
        country = self.cleaned_data['country']
        if country == None:
            raise forms.ValidationError(_('This field is required.'))
        return country  
    
    def clean_country_code(self):
        country_code = self.cleaned_data['country_code']
        if len(str(country_code)) > 3:
            raise forms.ValidationError(_('Please enter maximum 3 characters.'))
        if len(str(country_code)) < 2:
            raise forms.ValidationError(_('Please enter minimum 2 characters.'))
        return country_code 
    
    def clean_number_of_clients(self):
        number_of_clients = self.cleaned_data['number_of_clients']
        if len(str(number_of_clients)) > 3:
            raise forms.ValidationError(_('Enter no more than 3 characters.'))
        return number_of_clients 
    
    def clean_company_number(self):
        company_number = self.cleaned_data['company_number']
        qs = User.objects.filter(username = company_number)
        if self.id:
            qs = qs.exclude(username = self.company_number)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Number is already in use.'))
        
        if len(company_number) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        elif  re.match(r'^[\s]*$', company_number):
            raise forms.ValidationError(_("Enter a valid Company Number."))        
        return company_number
    
    def clean_sub_domain(self):
        sub_domain = self.cleaned_data['sub_domain']
        qs = Company.objects.filter(sub_domain = sub_domain)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('Sub-Domain Already Exits.'))
        if len(sub_domain) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', sub_domain):
            raise forms.ValidationError(_("Enter a valid Sub-Domain."))
        if not re.match(r'^[\sA-Za-z,0-9]+(?:[\s-][A-Za-z\s]+)*$', sub_domain):
            raise forms.ValidationError(_('Alphabets and Numbers Only.'))
        reserved = ['admin','administrator']
        if " ".join(sub_domain.split()) in reserved:
            raise forms.ValidationError(_("This is a reserved word."))
        return sub_domain 
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone_number = mobile_number_validation(phone_number)
        if not phone_number:
            raise forms.ValidationError(_("Enter a valid contact number"))
        return phone_number      