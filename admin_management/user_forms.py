import re 

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from vcg.admin_management.models import AdminUser, AdminUserPermission


attrs_dict = {'class': 'required'} 
USERNAME_RE = r'^[\.\w]+$'

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = AdminUser    

    def __init__(self, *args, **kw):
        super(AdminUserForm, self).__init__(*args, **kw)
        self.fields['first_name'].widget.attrs['class']   = 'form-text'
        self.fields['last_name'].widget.attrs['class']    = 'form-text'
        self.fields['email'].widget.attrs['class'] = 'form-text'
        self.fields['user_id'].widget.attrs['class'] = 'form-text'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        admin_user = AdminUser.objects.filter(email = email)
        if not admin_user:
            user = User.objects.filter(email = email)
            if user:
                raise forms.ValidationError(_('Email Already Exits.'))
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', first_name):
            raise forms.ValidationError(_("Enter a valid name."))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 3:
            raise forms.ValidationError(_('Enter minimum 3 characters.'))
        elif  re.match(r'^[\s]*$', last_name):
            raise forms.ValidationError(_("Enter a valid name."))
        return last_name

class AdminUserPermissionForm(forms.ModelForm):
    class Meta:
        model = AdminUserPermission
        
    def __init__(self, *args, **kw):
        super(AdminUserPermission, self).__init__(*args, **kw)    
        
class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length = 20 )

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']       = 'form-text'
        self.fields['username'].widget.attrs['placeholder'] = _('UserName')
        
    def clean_username(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        username = self.cleaned_data["username"]
        self.users_cache = User.objects.filter(
                                username__iexact=username,
                                is_active=True
                            )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That UserName doesn't have an associated user account. Are you sure you are registered?"))
        return username