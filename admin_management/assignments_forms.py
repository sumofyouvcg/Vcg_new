import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from vcg.admin_management.models import Assignment, AssignmentCluster, AssignmentQuestion, AssignmentQuestionAnswer

class AssignmentsForm(forms.ModelForm):
    class Meta:
        model = Assignment
    
    def __init__(self, *args, **kw):
        super(AssignmentsForm, self).__init__(*args, **kw)
        self.fields['name'].widget.attrs['class'] = 'form-text'
        self.fields['summary'].widget.attrs['class'] = 'form-textareas'
        
    def clean_name(self):
        assignment = self.cleaned_data['name']
        if len(assignment) < 3:
            raise forms.ValidationError(_('Enter more than 2 characters.'))
        elif  re.match(r'^[\s]*$', assignment):
            raise forms.ValidationError(_('Enter a valid assignment name.'))
        elif not re.match(r'^[\sA-Za-z,0-9]+(?:[\s-][A-Za-z\s]+)*$', assignment):
            raise forms.ValidationError(_('Alphabets and Numbers Only.'))
        return assignment
    
    def clean_summary(self):
        summary = self.cleaned_data['summary']
        if len(summary) < 11:
            raise forms.ValidationError(_('Enter minimum 10 characters.'))
        elif  re.match(r'^[\s]*$', summary):
            raise forms.ValidationError(_("Enter a valid summary."))
        return summary 
    
class AssignmentClusterForm(forms.ModelForm):
    class Meta:
        model = AssignmentCluster
    
    def __init__(self, *args, **kw):
        super(AssignmentClusterForm, self).__init__(*args, **kw)
        self.fields['assignment'].widget.attrs['class'] = 'form-dropdownfield'
        self.fields['cluster_name'].widget.attrs['class'] = 'form-text'
    
        if 'instance' in kw:
            self.id = kw['instance'].id
            self.assignment = kw['instance'].assignment
        else:
            self.id = ""     
            self.assignment = "" 
                    
    def clean_cluster_name(self):
        assignment = self.cleaned_data['cluster_name']
        if len(assignment) < 5:
            raise forms.ValidationError(_('Enter more than 4 characters.'))
        elif  re.match(r'^[\s]*$', assignment):
            raise forms.ValidationError(_('Enter a valid assignment name.'))
        elif not re.match(r'^[\sA-Za-z,0-9]+(?:[\s-][A-Za-z\s]+)*$', assignment):
            raise forms.ValidationError(_('Alphabets and Numbers Only.'))
        return assignment
    
    def clean(self):
        assignment      = self.cleaned_data.get("assignment")
        cluster_name    = self.cleaned_data.get("cluster_name")
        qs  = AssignmentCluster.objects.filter(cluster_name = cluster_name, assignment = assignment)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('Cluster Name Already Exists.'))  
        return self.cleaned_data 
    
class AssignmentQuestionForm(forms.ModelForm):
    class Meta:
        model = AssignmentQuestion
    
    def __init__(self, *args, **kw):
        super(AssignmentQuestionForm, self).__init__(*args, **kw)
        self.fields['assignment_cluster'].widget.attrs['class'] = 'form-dropdownfield'
        self.fields['question_text'].widget.attrs['class'] = 'form-text'
        
    def clean_question_text(self):
        title = self.cleaned_data['question_text']
        if len(title) < 11:
            raise forms.ValidationError(_('Enter more than 10 characters.'))
        elif  re.match(r'^[\s]*$', title):
            raise forms.ValidationError(_('Enter a valid title.'))
        return title
    
class AssignmentQuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = AssignmentQuestionAnswer
    
    def __init__(self, *args, **kw):
        super(AssignmentQuestionAnswerForm, self).__init__(*args, **kw)
        self.fields['assignment_question'].widget.attrs['class'] = 'form-dropdownfield'
        self.fields['option'].widget.attrs['class'] = 'form-text'
        
    def clean_option(self):
        assignment = self.cleaned_data['option']
        if len(assignment) < 3:
            raise forms.ValidationError(_('Enter more than 2 characters.'))
        elif  re.match(r'^[\s]*$', assignment):
            raise forms.ValidationError(_('Enter a valid assignment name.'))
        elif not re.match(r'^[\sA-Za-z,0-9]+(?:[\s-][A-Za-z\s]+)*$', assignment):
            raise forms.ValidationError(_('Alphabets and Numbers Only.'))
        return assignment
    
class QuestionAnswerForm(forms.Form):
    question = forms.CharField(help_text = _("Tick the correct answer"), max_length = 500, label = _('Question*'))
    choice_a = forms.CharField(max_length = 100, label = _('Choice A*'))
    answer_a = forms.BooleanField(required=False)
    choice_b = forms.CharField(max_length = 100, label = _('Choice B*'))
    answer_b = forms.BooleanField(required=False)
    choice_c = forms.CharField(max_length = 100, label = _('Choice C*'))
    answer_c = forms.BooleanField(required=False)
    choice_d = forms.CharField(max_length = 100, label = _('Choice D*'))
    answer_d = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kw):
        super(forms.Form, self).__init__(*args, **kw)
        self.fields['answer_a'].widget.attrs['class'] = 'answer'
        self.fields['answer_b'].widget.attrs['class'] = 'answer'
        self.fields['answer_c'].widget.attrs['class'] = 'answer'
        self.fields['answer_d'].widget.attrs['class'] = 'answer'
        self.fields['question'].widget.attrs['class'] = 'form-text'
        
    def clean_question(self):
        title = self.cleaned_data['question']
        if len(title) < 11:
            raise forms.ValidationError(_('Enter more than 10 characters.'))
        elif  re.match(r'^[\s]*$', title):
            raise forms.ValidationError(_('Enter a valid title.'))
        return title
