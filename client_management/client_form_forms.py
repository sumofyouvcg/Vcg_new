import re

from django import forms
from django.utils.translation import ugettext as _

from vcg.client_management.models import CompanyFormFeedback

class CompanyFormFeedbackForm(forms.ModelForm):
    class Meta:
        model = CompanyFormFeedback    

    def __init__(self, *args, **kw):
        super(CompanyFormFeedbackForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 

        self.fields['client_intake_form'].widget.attrs['class']  = 'form-dropdownfield'
        self.fields['feedback'].widget.attrs['class']            = 'form-textarea-feed'
        
    def clean_feedback(self):
        feedback = self.cleaned_data['feedback']
        if len(feedback) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', feedback):
            raise forms.ValidationError(_("Enter a valid address."))
        return feedback   
