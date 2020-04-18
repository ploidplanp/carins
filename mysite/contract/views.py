import json
# -----------------
from builtins import object
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.expressions import OrderBy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.views.decorators.csrf import csrf_exempt

from contract.models import (Car, Compulsory_Insurance, Contract, Customer,
                             Insurance_Policy, Owner)
from home.models import (Brand, Car_Use_Type_Table, Company, Person,
                         Premium_Table, Province)
from home.views import profile

from .forms import Insurance_PolicyFrom


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


@login_required
# หน้าเพิ่มกรมธรรม์ ประกัน
def new_policy(request):
    companylist = Company.objects.all()
    caruselist = Car_Use_Type_Table.objects.all().order_by('code')
    if request.method == 'POST':
        form = Insurance_PolicyFrom(request.POST)
        if form.is_valid():
            print(form.cleaned_data) # ทั้งก้อน
        else:
            print('invalid')
    else:
        form = Insurance_PolicyFrom()
        print('nothing')

    context = {
        'form': form,
        'companylist': companylist,
        'caruselist': caruselist
    }
    return render(request, 'insurance_policy/new_policy.html', context=context)


@login_required
# หน้าเพิ่มกรมธรรม์ พ.ร.บ.
def new_compulsory(request):
    return render(request, 'compulsory_insurance/new_compulsory.html')


def contract_search(request):
    userid = request.user.id
    me = Person.objects.get(user_id=userid) #ตัวเรา=userที่ login
    takecare = Customer.objects.filter(seller_id=me.id) #ลูกค้าที่ userดูแล
    takecarelistid = []
    for i in takecare:
        takecarelistid.append(i.id)
    # takecarelistid คือ ไอดีลูกค้าที่ user ดูแล

    #กรมธรรม์ทั้งหมดของลูกค้าที่ user ดูแล และเพิ่ม3 วันล่าสุด
    cusbuycontract = Contract.objects.filter(customer_id__in=takecarelistid, register_date__gte=date.today() - timedelta(days=3))
    cusbuycontractlistid = [] 
    for i in cusbuycontract:
        cusbuycontractlistid.append(i) #ไอดีกรมธรรม์ทั้งหมดที่ลูกค้าที่ user ดูแล

    # print('ลูกค้าที่ซื้อพรบ')
    cusbuycoumpulsory = Compulsory_Insurance.objects.filter(contract_id__in=cusbuycontractlistid)
    # print('ลูกค้าที่ซื้อประกัน')
    cusbuyinsurance = Insurance_Policy.objects.filter(contract_id__in=cusbuycontractlistid)

    context = {
        'cusbuycoumpulsory': cusbuycoumpulsory,
        'cusbuyinsurance': cusbuyinsurance
    }
    return render(request, 'contract.html', context=context)




# request ข้อมูล ajax
@csrf_exempt
def getowner(request):
    data = json.loads(request.body)
    cardid = data['owner_cardid']
    find = 'no'
    try:
        owner = Owner.objects.get(card_id=cardid)
        ownername = owner.fname
        ownersur = owner.lname
        ownerphone = owner.phone
        owneraddress = owner.address
        find = 'yes'
    except Owner.DoesNotExist:
        print('no')
        ownername = ''
        ownersur = ''
        ownerphone = ''
        owneraddress = ''

    response = {
        'find': find,
        'name': ownername,
        'sur': ownersur,
        'phone': ownerphone,
        'address': owneraddress
    }
    
    return JsonResponse(response, status=200)

@csrf_exempt
def getcus(request):
    data = json.loads(request.body)
    name = data['cus_fname']
    sur = data['cus_lname']
    find = 'no'
    try:
        cus = Customer.objects.get(fname=name, lname=sur)
        print(cus)
        cuscardid = cus.card_id
        cusphone = cus.phone
        cusaddress = cus.address
        find = 'yes'
    except Customer.DoesNotExist:
        print('no')
        cuscardid = ''
        cusphone = ''
        cusaddress = ''

    response = {
        'find': find,
        'cardid': cuscardid,
        'phone': cusphone,
        'address': cusaddress
    }
    
    return JsonResponse(response, status=200)

@csrf_exempt
def getcar(request):
    data = json.loads(request.body)
    license = data['car_license']
    province = data['car_province']
    ctype = data['car_type']

    find = 'no'

    try:
        car = Car.objects.get(license_on=license, province=province, type=ctype)
        regist = car.date_register
        brand = car.brand_id
        model = car.model
        chassis = car.chassis_on
        displacement = car.displacement
        gvw = car.gvw
        seat = car.seat
        find = 'yes'
    except Car.DoesNotExist:
        regist = ''
        brand = 1
        model = ''
        chassis = ''
        displacement = ''
        gvw = ''
        seat = ''

    response = {
        'find': find,
        'regist': regist,
        'brand': brand,
        'model': model,
        'chassis': chassis,
        'displacement': displacement,
        'gvw': gvw,
        'seat': seat
    }
    
    return JsonResponse(response, status=200)
