import re

from django import forms
from django.utils.translation import ugettext as _

from vcg.admin_management.models import CreateQuestion, CreateQuestionChoice, CreateQuestionSlider, Module

class CreateQuestionForm(forms.ModelForm):
    
    class Meta:
        model = CreateQuestion
        
    def __init__(self, *args, **kwargs):
        super(CreateQuestionForm, self).__init__(*args, **kwargs)
        self.fields['question_text'].widget.attrs['class'] = 'form-text'
        self.fields['module'].widget.attrs['class'] = 'form-dropdownfield'
        self.fields['help_text'].widget.attrs['class'] = 'form-text'
        self.fields['answer_type'].widget.attrs['class'] = 'form-dropdownfield'
        
        self.fields['module'].queryset = Module.objects.filter(active = True)
        
    def clean_help_text(self):
        help_text = self.cleaned_data['help_text']
        if len(help_text) < 7:
            raise forms.ValidationError(_('Enter more than 6 characters.'))
        elif  re.match(r'^[\s]*$', help_text):
            raise forms.ValidationError(_("Enter a valid help_text."))
        return help_text
    
    def clean_module(self):
        name = self.cleaned_data['module']
        if name == '0':
            raise forms.ValidationError(_('This field is required.'))
        return name
    
    def clean_question_text(self):
        title = self.cleaned_data['question_text']
        if len(title) < 10:
            raise forms.ValidationError(_('Enter more than 9 characters.'))
        elif  re.match(r'^[\s]*$', title):
            raise forms.ValidationError(_('Enter a valid title.'))
        return title
    
    def clean_answer_type(self):
        answer_type = self.cleaned_data['answer_type']
        if answer_type == "0":
            raise forms.ValidationError(_('This field is required.'))
        return answer_type     

class CreateQuestionChoiceForm(forms.ModelForm):
    class Meta:
        model = CreateQuestionChoice
        
    def __init__(self, *args, **kwargs):
        super(CreateQuestionChoiceForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs['class']       = 'form-textarea'
        self.fields['answer'].widget.attrs['maxlength']        = '150'
        
    def clean_answer(self):
        answer = self.cleaned_data['answer']
        if len(answer) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', answer):
            raise forms.ValidationError(_("Enter a valid answer."))
        return answer 
    
class CreateQuestionSliderForm(forms.ModelForm):
    class Meta:
        model = CreateQuestionSlider
        
    def __init__(self, *args, **kwargs):
        super(CreateQuestionSliderForm, self).__init__(*args, **kwargs)

        self.fields['min_value'].widget.attrs['class']       = 'form-text'
        self.fields['max_value'].widget.attrs['class']      = 'form-text'

    def clean_min_value(self):
        min_value = self.cleaned_data['min_value']
        if len(str(min_value)) > 3:
            raise forms.ValidationError(_('Maximum 3 digits only.'))
        return min_value

    def clean_max_value(self):
        max_value = self.cleaned_data['max_value']
        if not max_value:
            raise forms.ValidationError(_('Maximum value must be greater than 1.'))
        if len(str(max_value)) > 3:
            raise forms.ValidationError(_('Maximum 3 digits only.'))
        return max_value  
      
    def clean(self):
        min_value      = self.cleaned_data.get("min_value")
        max_value    = self.cleaned_data.get("max_value")
        if min_value and max_value:
            if min_value >= max_value:
                raise forms.ValidationError(_('Maximum value must be greater than minimum value.'))
        return self.cleaned_data
