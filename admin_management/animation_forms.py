import re

from django import forms
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Animation

class AnimationForm(forms.ModelForm):
    class Meta:
        model = Animation
    
    def __init__(self, *args, **kwargs):
        super(AnimationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-text'

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 4:
            raise forms.ValidationError(_('Enter more than 3 characters.'))
        elif len(name) > 40:
            raise forms.ValidationError(_('Enter no more than 40 characters.'))
        elif  re.match(r'^[\s]*$', name):
            raise forms.ValidationError(_("Enter a valid name."))
        return name   
    
    def clean_location(self):
        animation = self.cleaned_data['location']
        if str(animation).split('.')[-1] not in ('swf', 'gif', ):
            raise forms.ValidationError(_('Upload *.swf or *.gif files only.'))
        return animation
