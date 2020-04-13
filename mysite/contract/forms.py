from django import forms

class TryForm(forms.Form):
    name = forms.CharField(label='Your name ', max_length=100)
    nickname = forms.CharField(label='Your nickname ', max_length=5)

# class Contract():