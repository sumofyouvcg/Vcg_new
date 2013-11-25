import re 
import datetime

from django import forms
from django.contrib.auth.models import User

from vcg.util.forms import mobile_number_validation
from vcg.admin_management.models import Caregiver, Company, Client, AdminUser
from django.utils.translation import ugettext as _

class CaregiversForm(forms.ModelForm):
    class Meta:
        model = Caregiver
        
    def __init__(self, *args, **kwargs):
        super(CaregiversForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(active =True)
        
        self.fields['name'].widget.attrs['class']               = 'form-text'
        self.fields['sur_name'].widget.attrs['class']           = 'form-text'
        self.fields['last_name'].widget.attrs['class']          = 'form-text'
        self.fields['address'].widget.attrs['class']            = 'form-textarea'
        self.fields['zip_code'].widget.attrs['class']           = 'form-text'
        self.fields['place_name'].widget.attrs['class']         = 'form-text'
        self.fields['country'].widget.attrs['class']            = 'form-dropdownfield'
        self.fields['email'].widget.attrs['class']              = 'form-text'
        self.fields['dob'].widget.attrs['class']                = 'datepicker'
        self.fields['gender'].widget.attrs['class']             = 'form-dropdownfield'
        self.fields['country_code'].widget.attrs['class']       = 'form-text-small'
        self.fields['phone_number'].widget.attrs['class']       = 'form-text-phone'
        self.fields['company'].widget.attrs['class']            = 'form-dropdownfield'
        self.fields['caregiver_number'].widget.attrs['class']   = 'form-text'
        self.fields['role'].widget.attrs['class']               = 'form-dropdownfield'
        self.fields['active'].widget.attrs['maxlength']         = '150'        
        
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id
            self.caregiver_number = kwargs['instance'].caregiver_number
        else:
            self.id = ""     
            self.caregiver_number = "" 
   
    
    def clean(self):
        email      = self.cleaned_data.get("email")
        company    = self.cleaned_data.get("company")
        if company:
            caregiver  = Caregiver.objects.filter(company = company, email = email)
            client     = Client.objects.filter(company = company, email = email)
            company    = Company.objects.filter(sub_domain = company.sub_domain, email = email)
            
            admin_user = AdminUser.objects.filter(email = email)
            if client or company or admin_user:
                raise forms.ValidationError(_('Email Already Exists.'))
            else:
                if self.id:
                    caregiver = caregiver.exclude(pk=self.id)
                if caregiver.count() > 0:
                    if not self.id:
                        raise forms.ValidationError(_('Email Already Exists.'))
                    else:
                        if not self.id == caregiver[0].id:  
                            raise forms.ValidationError(_('Email Already Exists.'))
        return self.cleaned_data             
       
        
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', name):
            raise forms.ValidationError(_("Enter a valid name."))
        elif not re.match(r'^[\sA-Za-z]+(?:[\s-][A-Za-z\s]+)*$', name):
            raise forms.ValidationError(_('Alphabet characters only.'))
        return name   
    
    def clean_sur_name(self):
        sur_name = self.cleaned_data['sur_name']
        if sur_name:
            if len(sur_name) < 3:
                raise forms.ValidationError(_('Enter minimum 3 characters.'))
            elif  re.match(r'^[\s]*$', sur_name):
                raise forms.ValidationError(_("Enter a valid name."))
            elif not re.match(r'^[\sA-Za-z]+(?:[\s-][A-Za-z\s]+)*$', sur_name):
                raise forms.ValidationError(_('Alphabet characters only.'))
        return sur_name 

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', last_name):
            raise forms.ValidationError(_("Enter a valid name."))
        elif not re.match(r'^[\sA-Za-z]+(?:[\s-][A-Za-z\s]+)*$', last_name):
                raise forms.ValidationError(_('Alphabet characters only.'))
        return last_name 
    
    def clean_address(self):
        address = self.cleaned_data['address']
        if len(address) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        elif  re.match(r'^[\s]*$', address):
            raise forms.ValidationError(_("Enter a valid address."))
        return address 

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if len(zip_code) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', zip_code):
            raise forms.ValidationError(_("Enter a valid ZIP Code."))
        return zip_code 
       
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
    
    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob != None:
            if dob > datetime.date.today():
                raise forms.ValidationError(_("Date cannot be in future"))
            return dob
    
    def clean_country_code(self):
        country_code = self.cleaned_data['country_code']
        if len(str(country_code)) > 5:
            raise forms.ValidationError(_('Enter no more than 5 characters.'))
        return country_code 
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone_number = mobile_number_validation(phone_number)
        if not phone_number:
            raise forms.ValidationError(_("Enter a valid contact number"))
        return phone_number 
    
    def clean_role(self):
        roles = self.cleaned_data['role']
        if len(roles) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', roles):
            raise forms.ValidationError(_("Enter a valid roles."))
        elif not re.match(r'^[\sA-Za-z]+(?:[\s-][A-Za-z\s]+)*$', roles):
            raise forms.ValidationError(_('Alphabet characters only.'))
        return roles

    def clean_caregiver_number(self):
        caregiver_number = self.cleaned_data['caregiver_number']
        qs = User.objects.filter(username = caregiver_number)
        if self.id:
            qs = qs.exclude(username = self.caregiver_number)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Number is already in use.'))
         
        if len(caregiver_number) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        elif  re.match(r'^[\s]*$', caregiver_number):
            raise forms.ValidationError(_("Enter a valid Caregiver Number."))
        return caregiver_number
