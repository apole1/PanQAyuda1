from django import forms
from core.models import UserProfileInfo
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password', 'email')
        labels = {
            'username': _('Usuario'),
            'password': _('Password'),
            'email': _('Correo'),
        }

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')