import re
from django import forms
from django.utils.translation import ugettext as _

from vcg.util.forms import HorizontalRadioRenderer
from vcg.client_management.models import ClientPlan, PlanFeedback

CHOICES = (('Yes', 'Yes',), ('No', 'No',))

class ClientPlanForm(forms.ModelForm):
    achieved = forms.ChoiceField(initial=0, widget = forms.RadioSelect(renderer = HorizontalRadioRenderer), choices=CHOICES)
    class Meta:
        model = ClientPlan    

    def __init__(self, *args, **kw):
        super(ClientPlanForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 

        self.fields['plan'].widget.attrs['class']               = 'form-dropdownfield'
        self.fields['action'].widget.attrs['class']             = 'form-text'
        self.fields['description'].widget.attrs['class']        = 'form-textareas'
        
    def clean_action(self):
        action = self.cleaned_data['action']
        if len(action) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', action):
            raise forms.ValidationError(_("Enter a valid name."))
        return action 
    
    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 10:
            raise forms.ValidationError(_('Enter minimum 10 characters.'))
        elif  re.match(r'^[\s]*$', description):
            raise forms.ValidationError(_("Enter a valid address."))
        return description
    
class PlanFeedbackForm(forms.ModelForm):
    class Meta:
        model = PlanFeedback    

    def __init__(self, *args, **kw):
        super(PlanFeedbackForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 

        self.fields['plan'].widget.attrs['class']               = 'form-dropdownfield'
        self.fields['feedback'].widget.attrs['class']           = 'form-textarea-feed'
        
    def clean_feedback(self):
        feedback = self.cleaned_data['feedback']
        if len(feedback) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', feedback):
            raise forms.ValidationError(_("Enter a valid address."))
        return feedback      