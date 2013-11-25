import re 
import datetime

from django import forms
from django.utils.translation import ugettext as _

from vcg.util.forms import mobile_number_validation
from vcg.company_management.models import ConfigurationContact, ConfigurationLogo, ConfigurationHomepage, ConfigurationLocation

class ConfigurationContactForm(forms.ModelForm):
    class Meta:
        model = ConfigurationContact
        
    def __init__(self, *args, **kwargs):
        super(ConfigurationContactForm, self).__init__(*args, **kwargs)
        
        self.fields['company'].widget.attrs['class']                    = 'form-dropdownfield'
        self.fields['name_of_institution'].widget.attrs['class']        = 'form-text'
        self.fields['email_external'].widget.attrs['class']             = 'form-text'
        self.fields['country_code_external'].widget.attrs['class']      = 'form-text-small'
        self.fields['phone_number_external'].widget.attrs['class']      = 'form-text-phone'
        self.fields['email_internal'].widget.attrs['class']             = 'form-text'
        self.fields['country_code_internal'].widget.attrs['class']      = 'form-text-small'
        self.fields['phone_number_internal'].widget.attrs['class']      = 'form-text-phone'

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id
        else:
            self.id = ""     
    def clean(self):
        phone_number_external      = self.cleaned_data.get("phone_number_external")
        country_code_external      = self.cleaned_data.get("country_code_external")
        
        phone_number_internal      = self.cleaned_data.get("phone_number_internal")
        country_code_internal      = self.cleaned_data.get("country_code_internal")
        
        if phone_number_external and not country_code_external:
            raise forms.ValidationError(_('External Country code Field is required .'))        
        if country_code_external and not phone_number_external:
            raise forms.ValidationError(_('External Phone Number Field is required .'))        

        if phone_number_internal and not country_code_internal:
            raise forms.ValidationError(_('Internal Country code Field is required .'))        
        if country_code_internal and not phone_number_internal:
            raise forms.ValidationError(_('Internal Phone Number Field is required .'))  
        
        return self.cleaned_data 
    
    def clean_name_of_institution(self):
        name_of_institution = self.cleaned_data['name_of_institution']
        if name_of_institution:
            if len(name_of_institution) < 3:
                raise forms.ValidationError(_('Enter minimum 3 characters.'))
            elif  re.match(r'^[\s]*$', name_of_institution):
                raise forms.ValidationError(_("Enter a valid name."))
        return name_of_institution  

    def clean_country_code_external(self):
        country_code_external = self.cleaned_data['country_code_external']
        if country_code_external:
            if len(str(country_code_external)) > 5:
                raise forms.ValidationError(_('maximum 5 characters.'))
        return country_code_external 
    
    def clean_phone_number_external(self):
        phone_number_external = self.cleaned_data['phone_number_external']
        if phone_number_external:
            phone_number_external = mobile_number_validation(phone_number_external)
            if not phone_number_external:
                raise forms.ValidationError(_("Enter a valid contact number"))
        return phone_number_external 

    def clean_country_code_internal(self):
        country_code_internal = self.cleaned_data['country_code_internal']
        if country_code_internal:
            if len(str(country_code_internal)) > 5:
                raise forms.ValidationError(_('maximum 5 characters.'))
        return country_code_internal 
    
    def clean_phone_number_internal(self):
        phone_number_internal = self.cleaned_data['phone_number_internal']
        if phone_number_internal:
            phone_number_internal = mobile_number_validation(phone_number_internal)
            if not phone_number_internal:
                raise forms.ValidationError(_("Enter a valid contact number"))
        return phone_number_internal         

class ConfigurationLogoForm(forms.ModelForm):
    class Meta:
        model = ConfigurationLogo
        
    def __init__(self, *args, **kwargs):
        super(ConfigurationLogoForm, self).__init__(*args, **kwargs)
        
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id
        else:
            self.id = ""     
            
class ConfigurationHomepageForm(forms.ModelForm):
    class Meta:
        model = ConfigurationHomepage
        
    def __init__(self, *args, **kwargs):
        super(ConfigurationHomepageForm, self).__init__(*args, **kwargs)
        
        self.fields['company'].widget.attrs['class']                    = 'form-dropdownfield'
        self.fields['header'].widget.attrs['class']                     = 'form-text'
        self.fields['introduction'].widget.attrs['class']               = 'form-textarea'
        
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id
        else:
            self.id = ""

    def clean_header(self):
        header = self.cleaned_data['header']
        if header:
            if len(header) < 3:
                raise forms.ValidationError(_('Enter minimum 3 characters.'))
            elif  re.match(r'^[\s]*$', header):
                raise forms.ValidationError(_("Enter a valid name."))
        return header

    def clean_introduction(self):
        introduction = self.cleaned_data['introduction']
        if introduction:
            if len(introduction) < 10:
                raise forms.ValidationError(_('Enter minimum 10 characters.'))
            elif  re.match(r'^[\s]*$', introduction):
                raise forms.ValidationError(_("Enter a valid address."))
        return introduction       
                
class ConfigurationLocationForm(forms.ModelForm):
    class Meta:
        model = ConfigurationLocation
        
    def __init__(self, *args, **kwargs):
        super(ConfigurationLocationForm, self).__init__(*args, **kwargs)
        
        self.fields['company'].widget.attrs['class']                    = 'form-dropdownfield'
        self.fields['country'].widget.attrs['class']                    = 'form-dropdownfield'
        self.fields['continent'].widget.attrs['class']                  = 'form-dropdownfield'
        
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id
        else:
            self.id = ""                  