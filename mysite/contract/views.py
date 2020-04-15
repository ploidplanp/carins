from django.contrib.auth.decorators import login_required
from django.db.models.expressions import OrderBy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth.models import User

from contract.models import Car, Customer
from home.models import Brand, Company, Province, Premium_Table, Person

from .forms import Insurance_PolicyFrom, CustomerForm

# Create your views here.
@login_required
# หน้ารายงานกรมธรรม์หมดอายุ
def report_expire(request):
    return render(request, template_name='report_ex.html')

@login_required
# หน้าเพิ่มผู้ติดต่อ
def add_customer(request):
    person = Person.objects.get(user_id=request.user.id)
    print(person.id)
    msg = ''
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data) # ทั้งก้อน
            customer = Customer.objects.create(
                card_id = form.cleaned_data['card_id'],
                fname = form.cleaned_data['fname'],
                lname = form.cleaned_data['lname'],
                phone = form.cleaned_data['phone'],
                address = form.cleaned_data['address'],
                seller = person # คนที่ดูแลลูกค้ารายนี้ก็คือคนที่ลอคอินอยู่
            )
            msg = 'We have you:\'D'
    else:
        form = CustomerForm()
    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'customer_add.html', context=context)

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
    carlist = Car.objects.all().order_by('license_on')
    customerlist = Customer.objects.all().order_by('fname', 'lname')
    companylist = Company.objects.all().order_by('name')
    premiumlist = Premium_Table.objects.all().order_by('code')

    context = {
        'carlist': carlist,
        'customerlist': customerlist,
        'companylist': companylist,
        'premiumlist': premiumlist
    }
    return render(request, 'compulsory_insurance/new_compulsory.html', context=context)
