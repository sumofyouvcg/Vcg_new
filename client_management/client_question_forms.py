import re
from django import forms
from django.utils.translation import ugettext as _

from vcg.util.forms import HorizontalRadioRenderer
from vcg.client_management.models import ClientQuestions, ClientQuestionsFeedback

CHOICES = (('Yes', 'Yes',), ('No', 'No',))

class ClientQuestionsForm(forms.ModelForm):
    class Meta:
        model = ClientQuestions    

    def __init__(self, *args, **kw):
        super(ClientQuestionsForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 

        self.fields['question'].widget.attrs['class']               = 'form-text'
        self.fields['answer'].widget.attrs['class']        = 'form-text'
    
class ClientQuestionsFeedbackForm(forms.ModelForm):
    class Meta:
        model = ClientQuestionsFeedback    

    def __init__(self, *args, **kw):
        super(ClientQuestionsFeedbackForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 

        self.fields['feedback'].widget.attrs['class']           = 'form-textarea-feed'
        
    def clean_feedback(self):
        feedback = self.cleaned_data['feedback']
        if len(feedback) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', feedback):
            raise forms.ValidationError(_("Enter a valid address."))
        return feedback      