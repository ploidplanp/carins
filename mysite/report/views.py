from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request


# Create your views here.

@login_required
# หน้ารายงานกรมธรรม์หมดอายุ
def report_expire(request):
    return render(request, template_name='report_ex.html')