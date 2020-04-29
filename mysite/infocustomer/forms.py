from django import forms

class Edit(forms.Form):
    cardid = forms.CharField(label='Card-id', max_length=13)
    phone = forms.CharField(label='Phone', max_length=10)
    address = forms.CharField(label='Address', max_length=255)

class EditUser(forms.Form):
    cardid = forms.CharField(label='Card-id', max_length=13)
    phone = forms.CharField(label='Phone', max_length=10)
    email = forms.CharField(label='Email', max_length=255)

class EditCompany(forms.Form):
    taxno = forms.CharField(label='taxno', max_length=13)
    phone = forms.CharField(label='Phone', max_length=10)
    address = forms.CharField(label='Address', max_length=255)
