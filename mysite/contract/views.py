from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.context_processors import request

from .forms import TryForm, ContractForm

# Create your views here.

@login_required
# หน้ารายงานกรมธรรม์หมดอายุ
def report_expire(request):
    return render(request, template_name='report_ex.html')

@login_required
# หน้าเพิ่มกรมธรรม์ ประกัน
def new_policy(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])
            return HttpResponse('thank you')
    else:
        form = ContractForm()
    return render(request, 'insurance_policy/new_policy.html', {'form': form})

@login_required
# หน้าเพิ่มกรมธรรม์ พ.ร.บ.
def new_compulsory(request):
    return render(request, template_name='compulsory_insurance/new_compulsory.html')
