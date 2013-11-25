import re
from django import forms

from vcg.client_management.models import AnimationFeedback

class AnimationFeedbackForm(forms.ModelForm):
    class Meta:
        model = AnimationFeedback    

    def __init__(self, *args, **kw):
        super(AnimationFeedbackForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 

        self.fields['animation'].widget.attrs['class']               = 'form-dropdownfield'
        self.fields['feedback'].widget.attrs['class']           = 'form-textarea'