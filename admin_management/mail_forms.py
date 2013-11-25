import re 

from django import forms
from django.utils.translation import ugettext as _

from vcg.admin_management.models import MailConfiguration

class MailConfigurationForm(forms.ModelForm):
    class Meta:
        model = MailConfiguration
        
    def __init__(self, *args, **kwargs):
        super(MailConfigurationForm, self).__init__(*args, **kwargs)
        
        self.fields['english'].widget.attrs['class']            = 'form-textarea'
        self.fields['dutch'].widget.attrs['class']              = 'form-textarea'
        
    def clean_english(self):
        english = self.cleaned_data['english']
        if len(english) < 10:
            raise forms.ValidationError(_('Enter minimum 10 characters.'))
        elif  re.match(r'^[\s]*$', english):
            raise forms.ValidationError(_("Enter a valid message."))
        return english 
            
    def clean_dutch(self):
        dutch = self.cleaned_data['dutch']
        if len(dutch) < 10:
            raise forms.ValidationError(_('Enter minimum 10 characters.'))
        elif  re.match(r'^[\s]*$', dutch):
            raise forms.ValidationError(_("Enter a valid message."))
        return dutch             