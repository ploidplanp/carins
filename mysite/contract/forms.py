from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from psycopg2.sql import Placeholder

from contract.models import Compulsory_Insurance, Customer

from .models import Brand, Company, Province

type_choice = (
    ('รถยนต์', 'รถยนต์'), ('รถจักรยานยนต์', 'จักรยานยนต์')
)
inscode_choice = (
    ('1', '1'), ('2', '2'), ('3', '3'), ('3+', '3+')
)
province_choice = tuple(Province.objects.all().values_list())
brand_choice = tuple(Brand.objects.all().values_list())

class ContractForm(forms.Form):
    # ข้อมูลเจ้าของรถ
    owner_cardid = forms.CharField(label='เลขบัตรประชาชนเจ้าของรถ', max_length=13, widget=forms.TextInput(attrs={'class':'form-control'}))
    owner_fname = forms.CharField(label='ชื่อเจ้าของรถ', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    owner_lname = forms.CharField(label='นามสกุลเจ้าของรถ', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    owner_phone = forms.CharField(label='เบอร์โทรศัพท์', max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    owner_address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control' }), label='ที่อยู่')

    # ข้อมูลรถ
    car_license = forms.CharField(label='เลขทะเบียนรถ', max_length=7, widget=forms.TextInput(attrs={'class':'form-control'}))
    car_province = forms.ChoiceField(label='จังหวัด', choices=province_choice)
    car_type = forms.ChoiceField(label='ประเภทรถ', choices=type_choice)
    car_register = forms.DateField(label='วันที่จดทะเบียน', input_formats=['%Y-%m-%d'])
    car_brand = forms.ChoiceField(label='ยี่ห้อรถ', choices=brand_choice)
    car_model = forms.CharField(label='รุ่นรถ', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    car_chassis = forms.CharField(label='เลขตัวรถ', max_length=17, widget=forms.TextInput(attrs={'class':'form-control'}))
    car_displacement = forms.IntegerField(label='ขนาดเครื่อง')
    car_gvw = forms.IntegerField(label='น้ำหนักรวม')
    car_seat = forms.IntegerField(label='จำนวนที่นั่ง')
    
    # ข้อมูลประกัน
    contract_insid = forms.CharField(label='เลขที่กรมธรรม์ประกัน', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    contract_cover_start = forms.DateField(label='วันเริ่มคุ้มครอง', input_formats=['%Y-%m-%d'])
    contract_cover_end = forms.DateField(label='วันสิ้นสุดคุ้มครอง', input_formats=['%Y-%m-%d'])
    contract_price = forms.FloatField(label='ราคา')

    # ข้อมูลเจ้าของรถ
    cus_cardid = forms.CharField(label='เลขบัตรประชาชนลูกค้า', max_length=13, widget=forms.TextInput(attrs={'class':'form-control'}))
    cus_fname = forms.CharField(label='ชื่อลูกค้า', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    cus_lname = forms.CharField(label='นามสกุลลูกค้า', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    cus_phone = forms.CharField(label='เบอร์โทรศัพท์', max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    cus_address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control' }), label='ที่อยู่')

    car_register.widget.attrs.update({'class':'form-control', 'Placeholder':'YYYY-MM-DD'})
    contract_cover_start.widget.attrs.update({'class':'form-control', 'Placeholder':'YYYY-MM-DD'})
    contract_cover_end.widget.attrs.update({'class':'form-control', 'Placeholder':'YYYY-MM-DD'})
    car_province.widget.attrs.update({'class':'form-control'})
    car_type.widget.attrs.update({'class':'form-control'})
    car_brand.widget.attrs.update({'class':'form-control'})
    car_displacement.widget.attrs.update({'class':'form-control'})
    car_gvw.widget.attrs.update({'class':'form-control'})
    car_seat.widget.attrs.update({'class':'form-control'})
    contract_price.widget.attrs.update({'class':'form-control'})

    def clean_contract_cover_end(self):
        data = self.cleaned_data.get('contract_cover_end')
        if self.cleaned_data.get('contract_cover_start') >= data:
            raise ValidationError(
                'วันสิ้นสุดวันคุ้มครองต้องไม่ย้อนหลัง',
                code='invalid'
            )
        return data
