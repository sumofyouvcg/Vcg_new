import re

from django import forms
from django.utils.translation import ugettext as _

from vcg.ckeditor.widgets import CKEditorWidget
from vcg.admin_management.models import Module, Session, ModuleAnimation, Animation

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        
    def __init__(self, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-text'
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', name):
            raise forms.ValidationError(_("Enter a valid name."))
        elif not re.match(r'^[\sA-Za-z,0-9]+(?:[\s-][A-Za-z\s]+)*$', name):
            raise forms.ValidationError(_('Alphabets and Numbers Only.'))
        return name 
    
class SessionForm(forms.ModelForm):
    plaintext = forms.CharField(widget=CKEditorWidget(), required= False)
    class Meta:
        model = Session
        
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-text'
        self.fields['module'].widget.attrs['class'] = 'form-dropdownfield'
        
        self.fields['module'].queryset = Module.objects.filter(active = True)
        
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id
            self.name = kwargs['instance'].name
        else:
            self.id = ""     
            self.name = "" 
            
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', name):
            raise forms.ValidationError(_("Enter a valid name."))
        elif not re.match(r'^[\sA-Za-z,0-9]+(?:[\s-][A-Za-z\s]+)*$', name):
            raise forms.ValidationError(_('Alphabets and Numbers Only.'))
        return name 
    
    def clean_module(self):
        name = self.cleaned_data['module']
        if name == '0':
            raise forms.ValidationError(_('This field is required.'))
        return name
    
    def clean(self):
        session   = self.cleaned_data.get("name")
        module    = self.cleaned_data.get("module")
        qs  = Session.objects.filter(name = session, module = module)
        if self.id:
            qs = qs.exclude(pk=self.id)
        if qs.count() > 0:
            raise forms.ValidationError(_('This Session Already Exists for this Module.'))  
        return self.cleaned_data 

class ModuleAnimationForm(forms.ModelForm):
    class Meta:
        model = ModuleAnimation
    
    def __init__(self, *args, **kwargs):
        super(ModuleAnimationForm, self).__init__(*args, **kwargs)
        
        self.fields['animation'].queryset = Animation.objects.filter(active = True)
        self.fields['module'].queryset = Module.objects.filter(active = True)
        
        self.fields['animation'].widget.attrs['class'] = 'form-dropdownfield'
        self.fields['module'].widget.attrs['class'] = 'form-dropdownfield'
        
    def clean(self):
        animation = self.cleaned_data.get('animation')
        name = self.cleaned_data.get('module')
        module = ModuleAnimation.objects.filter(animation = animation, module = name)
        if module:
            raise forms.ValidationError(_('Animation with this Module already Exists.'))
        if animation == '0':
            raise forms.ValidationError(_('This field is required.'))
        if name == '0':
            raise forms.ValidationError(_('This field is required.'))
        return self.cleaned_data
