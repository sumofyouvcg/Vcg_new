from django import forms
from django.forms import fields
from django.utils.translation import ugettext as _

from vcg.config.choices import caregivers_role

class CaregiverAddForm(forms.Form):
    first_name             = fields.CharField(required = True)
    insertion              = fields.CharField(required = True)
    surname                = fields.CharField(required = True)
    active                 = fields.BooleanField(required = False)         
    email                  = fields.EmailField(required = True)
    picture                = fields.ImageField(required = False)
    description            = fields.CharField(widget = forms.Textarea, required = True)
    role                   = fields.ChoiceField(choices = caregivers_role, required = False)
    
    def clean_role(self):
        role = self.cleaned_data['role']
        if role == '0':
            raise forms.ValidationError(_('This field is required.'))
        return role              
    
    def __init__(self, *args, **kwargs):
        super(CaregiverAddForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-text'      
        self.fields['insertion'].widget.attrs['class'] = 'form-text'     
        self.fields['surname'].widget.attrs['class'] = 'form-text'     
        self.fields['email'].widget.attrs['class'] = 'form-text'     
        self.fields['description'].widget.attrs['class'] = 'form-textarea'     
        self.fields['role'].widget.attrs['class'] = 'form-dropdownfield'     