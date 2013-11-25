import re
import datetime

from django import forms
from vcg.util.forms import HorizontalRadioRenderer
from django.utils.translation import ugettext as _
from django.forms.widgets import CheckboxSelectMultiple
from vcg.client_management.models import TreatmentForm,CompanyTreatmentFormFeedback
from vcg.config.forms import contents_sessions, online_therapy, client_consultation, treat_domains, methods_techniques, domains_yes, indicator_treatment

class TreatmentFormForm(forms.ModelForm):
    contents_sessions   = forms.ChoiceField(initial=0, widget = forms.RadioSelect(renderer = HorizontalRadioRenderer), choices = contents_sessions, label =_('Contents sessions'))
    online_therapy      = forms.ChoiceField(initial=0, widget = forms.RadioSelect(renderer = HorizontalRadioRenderer), choices = online_therapy, label =_('Online therapy'),required = False)
    client_consultation = forms.ChoiceField(initial=0, widget = forms.RadioSelect(renderer = HorizontalRadioRenderer), choices = client_consultation, label =_('During the sessions, in consultation with the client make use of one or more of the following methods and / or applications.*'),required = False)
    methods_techniques  = forms.MultipleChoiceField( widget=CheckboxSelectMultiple, choices=methods_techniques, label = _('Which methods and techniques?'),required = False)
    treat_domains       = forms.ChoiceField(initial=0, widget = forms.RadioSelect(renderer = HorizontalRadioRenderer), choices = treat_domains,  label =_('Can treat domains are distinguished'),required = False)
    domains_yes         = forms.MultipleChoiceField(choices = domains_yes, widget=forms.CheckboxSelectMultiple(), label = _('If yes, which'),required = False)
    indicator_treatment = forms.MultipleChoiceField(choices = indicator_treatment, widget=forms.CheckboxSelectMultiple(), label = _('Indicator treatment duration'),required = False)
    
    class Meta:
        model = TreatmentForm    

    def __init__(self, *args, **kw):
        super(TreatmentFormForm, self).__init__(*args, **kw)

#Personal
        self.fields['client_name'].widget.attrs['class']                = 'form-text'
        self.fields['address'].widget.attrs['class']                    = 'form-textarea'
        self.fields['code_town'].widget.attrs['class']                  = 'form-text'
        self.fields['dob'].widget.attrs['class']                        = 'form-text'
        self.fields['bsn_number'].widget.attrs['class']                 = 'form-text'
        self.fields['date_treatment_agreement'].widget.attrs['class']   = 'form-text'
        self.fields['treatment_goal'].widget.attrs['class']             = 'form-textarea'
        self.fields['one_three_sessions'].widget.attrs['class']         = 'form-textarea'
        self.fields['three_nine_sessions'].widget.attrs['class']        = 'form-textarea'
        self.fields['less_nine_sessions'].widget.attrs['class']         = 'form-textarea'
        self.fields['notes'].widget.attrs['class']                      = 'form-textarea'
        self.fields['indicator_treatment'].widget.attrs['class']        = 'form-indicate'
        self.fields['specific_beliefs'].widget.attrs['class']           = 'form-textarea'
        self.fields['after_care_treatment'].widget.attrs['class']       = 'form-textarea'
        
    def clean_client_name(self):
        client_name = self.cleaned_data['client_name']
        if client_name:
            if len(client_name) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return client_name

    def clean_address(self):
        address = self.cleaned_data['address']
        if address:
            if len(address) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return address
        
    def clean_code_town(self):
        code_town = self.cleaned_data['code_town']
        if code_town:
            if len(code_town) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return code_town
    
    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob:
            if dob != None:
                if dob > datetime.date.today():
                    raise forms.ValidationError(_("Date cannot be in future"))
                return dob
                
        
    def clean_bsn_number(self):
        bsn_number = self.cleaned_data['bsn_number']
        if bsn_number:
            if len(bsn_number) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return bsn_number
        
    def clean_date_treatment_agreement(self):
        date_treatment_agreement = self.cleaned_data['date_treatment_agreement']
        if date_treatment_agreement:
            if len(date_treatment_agreement) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return date_treatment_agreement

        
    def clean_treatement_goal(self):
        treatement_goal = self.cleaned_data['treatement_goal']
        if treatement_goal:
            if len(treatement_goal) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return treatement_goal
        
    def clean_notes(self):
        notes = self.cleaned_data['notes']
        if notes:
            if len(notes) < 1:
                raise forms.ValidationError(_('Enter minimum 1 character.'))
            return notes                  
        
class CompanyTreatmentFormFeedbackForm(forms.ModelForm):
    class Meta:
        model = CompanyTreatmentFormFeedback    

    def __init__(self, *args, **kw):
        super(CompanyTreatmentFormFeedbackForm, self).__init__(*args, **kw)
        if 'instance' in kw:
            self.id = kw['instance'].id
        else:
            self.id = "" 

        self.fields['company_treatment_form'].widget.attrs['class']  = 'form-dropdownfield'
        self.fields['feedback'].widget.attrs['class']                         = 'form-textarea-feed'
        
    def clean_feedback(self):
        feedback = self.cleaned_data['feedback']
        if len(feedback) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', feedback):
            raise forms.ValidationError(_("Enter a valid address."))
        return feedback   
                                                                                        