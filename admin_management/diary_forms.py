import re

from django import forms
from django.utils.translation import ugettext as _

from vcg.admin_management.models import Diary, DiaryQuestion, QuestionChoice, QuestionSlider

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        
    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class']          = 'form-text'
        self.fields['diary_number'].widget.attrs['class']   = 'form-text'
        self.fields['image'].widget.attrs['class']          = 'form-text'
        
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id
        else:
            self.id = ""          
 
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'^[\s]*$', title):
            raise forms.ValidationError(_('Enter a valid Title.'))
        elif len(title) < 5:
            raise forms.ValidationError(_('Enter minimum 5 characters.'))
        elif not re.match(r'^[\sA-Za-z]+(?:[\s-][A-Za-z\s]+)*$', title):
            raise forms.ValidationError(_('Alphabet characters only.'))
        return title

    def clean_diary_number(self):
        diary_number = self.cleaned_data['diary_number']
        qs = Diary.objects.filter(diary_number = diary_number)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Number is already in use.')) 
        if len(diary_number) < 1:
            raise forms.ValidationError(_('Enter minimum 1 character.'))
        elif  re.match(r'^[\s]*$', diary_number):
            raise forms.ValidationError(_("Enter a valid Caregiver Number."))
        return diary_number    

class DiaryQuestionForm(forms.ModelForm):
    class Meta:
        model = DiaryQuestion
        
    def __init__(self, *args, **kwargs):
        super(DiaryQuestionForm, self).__init__(*args, **kwargs)

        self.fields['question'].widget.attrs['class']       = 'form-text'
        self.fields['help_text'].widget.attrs['class']      = 'form-text'
        self.fields['answer_type'].widget.attrs['class']    = 'form-dropdownfield'

    def clean_question(self):
        question = self.cleaned_data['question']
        if len(question) < 10:
            raise forms.ValidationError(_('Enter minimum 10 characters.'))
        return question   
    
    def clean_help_text(self):
        help_text = self.cleaned_data['help_text']
        if len(help_text) < 7:
            raise forms.ValidationError(_('Enter minimum 7 characters.'))
        return help_text
    
    def clean_answer_type(self):
        answer_type = self.cleaned_data['answer_type']
        if answer_type == "0":
            raise forms.ValidationError(_('This field is required.'))
        return answer_type     

class QuestionChoiceForm(forms.ModelForm):
    class Meta:
        model = QuestionChoice
        
    def __init__(self, *args, **kwargs):
        super(QuestionChoiceForm, self).__init__(*args, **kwargs)

        self.fields['answer'].widget.attrs['class']       = 'form-textarea'
        
class QuestionSliderForm(forms.ModelForm):
    class Meta:
        model = QuestionSlider
        
    def __init__(self, *args, **kwargs):
        super(QuestionSliderForm, self).__init__(*args, **kwargs)

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
