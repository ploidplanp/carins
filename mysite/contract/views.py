from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.context_processors import request

# Create your views here.

@login_required
# หน้ารายงานกรมธรรม์หมดอายุ
def report_expire(request):
    return render(request, template_name='report_ex.html')

@login_required
# หน้าเพิ่มกรมธรรม์ ประกัน
def new_policy(request):
    return render(request, template_name='insurance_policy/new_policy.html')

@login_required
# หน้าเพิ่มกรมธรรม์ พ.ร.บ.
def new_compulsory(request):
    return render(request, template_name='compulsory_insurance/new_compulsory.html')
