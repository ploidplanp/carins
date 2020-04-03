from django.shortcuts import render
from django.template.context_processors import request

# Create your views here.

def mylogin(request):
    context = {}
    return render(request, template_name='login.html')

# กดที่ home
def profile(request):
    return render(request, 'profile.html')

# กดที่ ดูข้อมูล เลือก บริษัท จะแสดงรายชื่อบริษัททั้งหมด
def company_detail(request):
    return render(request, 'company.html')

# กดที่ ดูข้อมูล เลือก ตารางอัตราเบี้ยพ.ร.บ.
def premium_detail(request):
    return render(request, 'premiumTable.html')

# กดที่ ดูข้อมูล เลือก ตารางรหัสการใช้รถ
def cartype_detail(request):
    return render(request, 'carUseType.html')
