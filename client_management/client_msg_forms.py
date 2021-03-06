import re

from django import forms
from django.forms import fields
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import ugettext as _

from vcg.company_management.models import Messages, SentMessages, ClientCaregivers
from vcg.admin_management.models import Client

class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages    
    
    def __init__(self, *args, **kw):

        user = kw.pop('user', None)
        client_user = Client.objects.filter(client_number = user.username)
        client_caregivers = []
        client_caregivers_list = ClientCaregivers.objects.filter(client__client_number = user.username)
        for client in client_caregivers_list:
            client_caregivers.append(client.caregiver.caregiver_number)
        
        super(MessagesForm, self).__init__(*args, **kw)
        
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = ""
                 
        if client_user:
            self.fields['recipient'].queryset = User.objects.filter(Q(username__in = client_caregivers)|Q(username = client_user[0].company.company_number))
       
        self.fields['recipient'].widget.attrs['class']          = 'form-dropdownfield'
        self.fields['title'].widget.attrs['class']              = 'form-text'
        self.fields['description'].widget.attrs['class']        = 'form-textarea'
        self.fields['attachment'].widget.attrs['class']         = 'form-text'
    
#    def user_unicode(self):
#        return self.first_name + ' (' + str(self.username) + ')'
#    User.__unicode__ = user_unicode

    def clean_recipient(self):
        name = self.cleaned_data['recipient']
        if name == '0':
            raise forms.ValidationError(_('This field is required.'))
        return name
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError(_('Enter more than 2 characters.'))
        elif  re.match(r'^[\s]*$', title):
            raise forms.ValidationError(_('Enter a valid title.'))
        return title
    
    def clean_description(self):
        address = self.cleaned_data['description']
        if len(address) < 10:
            raise forms.ValidationError(_('Enter more than 10 characters.'))
        elif  re.match(r'^[\s]*$', address):
            raise forms.ValidationError(_("Enter a valid description."))
        return address 

class SentMessagesForm(forms.ModelForm):
    class Meta:
        model = SentMessages    
    
    def __init__(self, *args, **kw):
#     
        user = kw.pop('user', None)
        client_user = Client.objects.filter(client_number = user.username)
        client_caregivers = []
        client_caregivers_list = ClientCaregivers.objects.filter(client__client_number = user.username)
        for client in client_caregivers_list:
            client_caregivers.append(client.caregiver.caregiver_number)
            
        super(SentMessagesForm, self).__init__(*args, **kw) 

        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = ""
                 
        if client_user:
            self.fields['recipient'].queryset = User.objects.filter(Q(username__in = client_caregivers)|Q(username = client_user[0].company.company_number))
            