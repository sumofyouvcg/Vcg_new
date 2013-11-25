import re

from django import forms
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan    

    def __init__(self, *args, **kw):
        super(PlanForm, self).__init__(*args, **kw)
        self.fields['title'].widget.attrs['class'] = 'form-text'
        self.fields['description'].widget.attrs['class'] = 'form-textareas'

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'^[\s]*$', title):
            raise forms.ValidationError(_('Enter a valid Title.'))
        elif len(title) < 5:
            raise forms.ValidationError(_('Enter minimum 5 characters.'))
        elif not re.match(r'^[\sA-Za-z]+(?:[\s-][A-Za-z\s]+)*$', title):
            raise forms.ValidationError(_('Alphabet characters only.'))
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 30:
            raise forms.ValidationError(_('Enter minimum 30 characters.'))
        elif len(description) > 500:
            raise forms.ValidationError(_('Enter maximum 500 characters only.'))
        return description
