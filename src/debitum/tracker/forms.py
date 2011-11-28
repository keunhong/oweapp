# coding=UTF-8

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

TYPE_CHOICES = (
    ('D', 'Debt'),
    ('P', 'Payment'),
)

class TransactionCreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': _(u"Title")}))
    recipient_email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': _(u"Recipient Email")}))
    transaction_type = forms.ChoiceField(choices=TYPE_CHOICES)
    amount = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea, label='Description')

class TransactionRevisionCreateForm(forms.Form):
    amount = forms.IntegerField()
    comment = forms.CharField(widget=forms.Textarea, label='Description')

class TransactionApproveForm(forms.Form):
    transaction_id = forms.IntegerField()
