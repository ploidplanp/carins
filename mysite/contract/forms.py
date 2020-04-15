from django import forms
from django.forms import ModelForm
from psycopg2.sql import Placeholder

# from .models import Contract, Insurance_Policy
from .models import Province
from contract.models import Compulsory_Insurance, Contract

type_choice = (
    ('รถยนต์', 'รถยนต์'), ('รถจักรยานยนต์', 'จักรยานยนต์')
)

class Insurance_PolicyFrom(forms.Form):
    owner_fname = forms.CharField(label='ชื่อเจ้าของรถ', max_length=255)
    owner_lname = forms.CharField(label='นามสกุล', max_length=255)
    license = forms.CharField(label='เลขทะเบียนรถ', max_length=7)

    car_register = forms.CharField(label='วันที่จดทะเบียน', max_length=7)
    model = forms.CharField(label='รุ่นรถ', max_length=255)
    cartype = forms.CharField(label='ประเภทรถ', max_length=13)
    displacement = forms.CharField(label='น้ำหนักรวม', max_length=7)
    gvw = forms.CharField(label='น้ำหนักรวม', max_length=10)
    seat = forms.CharField(label='น้ำหนักรวม', max_length=10)

    owner_card_id = forms.CharField(label='เลขบัตรประชาชนเจ้าของรถ', max_length=13)
    owner_address = forms.CharField(widget=forms.Textarea, label='ที่อยู่')
    owner_phone = forms.CharField(label='เบอร์โทรศัพท์', max_length=10)

    cus_fname = forms.CharField(label='ชื่อผู้ติดต่อ', max_length=13)
    cus_lname = forms.CharField(label='นามสกุล', max_length=13)
    cus_card_id = forms.CharField(label='เลขบัตรประชาชนผู้ติดต่อ', max_length=13)
    cus_address = forms.CharField(widget=forms.Textarea, label='ที่อยู่ผู้ติดต่อ', max_length=13)
    cus_phone = forms.CharField(label='เบอร์โทรศัพท์ผู้ติดต่อ', max_length=13)

    allfields = [owner_fname, owner_lname, license, car_register, model, cartype,
    displacement, gvw, seat, owner_card_id, owner_address, owner_phone, cus_fname, cus_lname,
    cus_card_id, cus_address, cus_phone]

    for i in allfields:
        i.widget.attrs.update({'class':'form-control'})

    license.widget.attrs.update({'class':'form-control', 'Placeholder':'อท1616'})

class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'