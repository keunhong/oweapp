# coding=UTF-8

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.Form):
    """
    Registration Form
    """
    email = forms.EmailField(label=_(u"Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(), label=_(u"Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(), label=_(u"Confirm Password"))
    first_name = forms.CharField(label=_(u"First Name"))
    last_name = forms.CharField(label=_(u"Last Name"))

    def clean_password(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError(_("Passwords must match"))
        return self.data['password1']

    def clean_email(self):
        email_exists = User.objects.filter(email__exact=self.data['email']).count() != 0

        if email_exists:
            raise forms.ValidationError(_("Email exists"))
        return self.data['email']

    def clean(self):
        self.clean_password()
        return super(RegistrationForm, self).clean()
