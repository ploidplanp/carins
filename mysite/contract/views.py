from django.contrib.auth.decorators import login_required
from django.db.models.expressions import OrderBy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.context_processors import request

from contract.models import Car, Customer
from home.models import Brand, Company, Province, Premium_Table

from .forms import ContractForm, Insurance_PolicyFrom

# Create your views here.
carlist = Car.objects.all().order_by('license_on')
customerlist = Customer.objects.all().order_by('fname', 'lname')
companylist = Company.objects.all().order_by('name')
premiumlist = Premium_Table.objects.all().order_by('code')


@login_required
# หน้ารายงานกรมธรรม์หมดอายุ
def report_expire(request):
    return render(request, template_name='report_ex.html')

@login_required
# หน้าเพิ่มกรมธรรม์ ประกัน
def new_policy(request):
    if request.method == 'POST':
        form = Insurance_PolicyFrom(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponse('thank you')
    else:
        form = Insurance_PolicyFrom()

    brandlist = Brand.objects.all()
    provincelist = Province.objects.all()
    context = {
        'form': form,
        'brandlist': brandlist,
        'provincelist': provincelist
    }
    return render(request, 'insurance_policy/new_policy.html', context=context)

@login_required
# หน้าเพิ่มกรมธรรม์ พ.ร.บ.
def new_compulsory(request):
    context = {
        'carlist': carlist,
        'customerlist': customerlist,
        'companylist': companylist,
        'premiumlist': premiumlist
    }
    return render(request, 'compulsory_insurance/new_compulsory.html', context=context)
