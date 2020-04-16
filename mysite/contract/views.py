# from os import name
# from os.path import normcase
from builtins import object
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.expressions import OrderBy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.context_processors import request

from contract.models import Car, Compulsory_Insurance, Contract, Customer
from home.models import Brand, Company, Person, Premium_Table, Province

from .forms import CustomerForm


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
    return render(request, 'management/customer_add.html', context=context)

def add_car(request):
    return render(request, 'management/car_add.html', context=context)


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
    provincelist = Province.objects.all().order_by('name')
    companylist = Company.objects.all().order_by('name')
    premiumlist = Premium_Table.objects.all().order_by('code')

    cusfname = request.POST.get('inputCusfname', '')
    cuslname = request.POST.get('inputCuslname', '')
    cus_mes = ''
    car_mes = ''

    carlicense = request.POST.get('inputLicense', '')
    carprovince = request.POST.get('inputProvince', '')
    
    ownerfname = request.POST.get('inputOwnfname', '')
    ownerlname = request.POST.get('inputOwnflname', '')

    contractno = request.POST.get('contractno', '')
    datecover = request.POST.get('datecover', '')
    company = request.POST.get('companySelect', '')
    premiumcode = request.POST.get('premiumSelect', '')
    

    if request.method == 'POST':
        if 'search_license' in request.POST and carprovince != "Choose...":
            print(carlicense)
            print(carprovince)
            try:
                car = Car.objects.get(license_on=carlicense, province=carprovince)
                carprovince = car.province.id
                ownerfname = car.owner.fname
                ownerlname = car.owner.lname
                car_mes = "car"
            except Car.DoesNotExist:
                car_mes = 'not'

        if 'search_customer' in request.POST:
            try:
                customer = Customer.objects.get(fname=cusfname, lname=cuslname)
                cus_mes = 'customer'
                car = Car.objects.get(license_on=carlicense, province=carprovince)
                carprovince = car.province.id
                ownerfname = car.owner.fname
                ownerlname = car.owner.lname
            except Customer.DoesNotExist:
                cus_mes = 'not'
    if 'new' in request.POST and (company != "Choose..." and premiumcode != 'Choose...' and contractno != '' and datecover != ''):
        print(datecover)
        print(contractno)
        print(company)
        print(premiumcode)

        datecover = datecover.split('-')
        print(datecover)
        datelist = []
        for i in datecover:
            if i == datecover[0]:
                datelist.append(int(i)+1)
            else:
                datelist.append(int(i))
        print(datelist[0])
        enddate = '%d-%d-%d' %(datelist[0], datelist[1], datelist[2])
            
        mycusid = Customer.objects.get(fname=cusfname, lname=cuslname)
        mycar = Car.objects.get(license_on=carlicense, province=carprovince)

        newcontract = Contract.objects.create(
            register_date = date.today(),
            status = 'Available',
            date_start_cover = datecover,
            date_end_cover = enddate,
            customer_id = mycusid.id,
            company_id = company,
            car_id = mycar.id
        )
        lastcontract = Contract.objects.latest('id')
        newcom = Compulsory_Insurance.objects.create(
            compulsory_id = contractno,
            compulsory_car_use_type_id = premiumcode,
            contract_id = lastcontract.id
        )

    print(type(date(2021, 2, 5)))
    print(type(datecover))

    context = {
        'provincelist': provincelist,
        'companylist': companylist,
        'premiumlist': premiumlist,
        'cus_mes': cus_mes,
        'cusfname': cusfname,
        'cuslname': cuslname,
        'car_mes': car_mes,
        'carlicense': carlicense,
        'carprovince': carprovince,
        'ownerfname': ownerfname,
        'ownerlname': ownerlname,
        'contractno': contractno,
        'datecover': datecover,
        'company': company,
        'premiumcode': premiumcode
    }
    return render(request, 'compulsory_insurance/new_compulsory.html', context=context)
