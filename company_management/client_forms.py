from django import forms
from django.forms import fields
from django.utils.translation import ugettext as _

from vcg.config.choices import caregiver_choices, diary_choices, company, treatment_module, treatment_guidence, treatment_sessions, motivation_plans

#old Forms        
class ClientMessageForm(forms.Form):
    title                     = fields.CharField(required = True)
    description               = fields.CharField(widget = forms.Textarea, required = True)
    attachment                = fields.FileField(required = False)
    

class ClientDiaryAddForm(forms.Form):
    diary                     = fields.ChoiceField(choices = diary_choices, required = False)
    caregiver                 = fields.ChoiceField(choices = caregiver_choices, required = False)

    def clean_diary(self):
        diary = self.cleaned_data['diary']
        if diary == '0':
            raise forms.ValidationError(_('This field is required.'))
        return diary  

    def clean_caregiver(self):
        caregiver = self.cleaned_data['caregiver']
        if caregiver == '0':
            raise forms.ValidationError(_('This field is required.'))
        return caregiver
