from django import forms
from django.forms import ModelForm

from .models import Contract, Insurance_Policy

class TryForm(forms.Form):
    name = forms.CharField(label='Your name ', max_length=100)
    nickname = forms.CharField(label='Your nickname ', max_length=5)

class ContractForm(ModelForm):
    class Meta:
        model = Contract
        exclude = ['register_date', 'status']

class Insurance_PolicyForm(ModelForm):
    class Meta:
        model = Insurance_Policy
        exclude = ['contract']