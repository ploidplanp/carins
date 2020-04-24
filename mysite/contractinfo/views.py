import json

from django.shortcuts import render
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

# Create your views here.


# หน้ารายการกรมธรรม์ประกัน
@login_required
def ins_search(request):
    print('yes')
    msg = ''
    searchcontractid = request.POST.get('contractid', '')
    searchlicense = request.POST.get('license', '')
    searchoname = request.POST.get('oname', '')
    searchosur = request.POST.get('osur', '')

    userid = request.user.id
    me = Person.objects.get(user_id=userid) #ตัวเรา=userที่ login
    takecare = Customer.objects.filter(seller_id=me.id) #ลูกค้าที่ userดูแล
    takecarelistid = []
    for i in takecare:
        takecarelistid.append(i.id)
    # takecarelistid คือ ไอดีลูกค้าที่ user ดูแล

    #กรมธรรม์ทั้งหมดของลูกค้าที่ user ดูแล และเพิ่ม7 วันล่าสุด
    cusbuycontract = Contract.objects.filter(customer_id__in=takecarelistid, register_date__gte=date.today() - timedelta(days=7))
    cusbuycontractlistid = [] 
    for i in cusbuycontract:
        cusbuycontractlistid.append(i) #ไอดีกรมธรรม์ทั้งหมดของลูกค้าที่ user ดูแล

     # print('ลูกค้าที่ซื้อประกัน')
    cusbuyinsurance = Insurance_Policy.objects.filter(contract_id__in=cusbuycontractlistid, contract__status='Available').order_by('-id')

    if request.method == 'POST':
        cusbuycontract = Contract.objects.filter(customer_id__in=takecarelistid)
        cusbuycontractlistid = [] 
        for i in cusbuycontract:
            cusbuycontractlistid.append(i) #ไอดีกรมธรรม์ทั้งหมดของลูกค้าที่ user ดูแล

        if 'search1' in request.POST and searchcontractid != '':
            cusbuyinsurance = Insurance_Policy.objects.filter(contract_id__in=cusbuycontractlistid, contract__status='Available', insurance_id=searchcontractid)
            msg = 'ค้นหากรมธรรม์เลขที่ %s' %(searchcontractid)
            print(cusbuyinsurance)
        elif 'search2' in request.POST and searchoname != '' and searchosur != '' and searchlicense != '':
            cusbuyinsurance = Insurance_Policy.objects.filter(contract_id__in=cusbuycontractlistid, contract__status='Available', contract__car__license_on=searchlicense, contract__car__owner__fname=searchoname, contract__car__owner__lname=searchosur)
            msg = 'ค้นหากรมธรรม์ทะเบียนรถ %s ผู้เอาประกัน %s %s' %(searchlicense, searchoname, searchosur)
            print(cusbuyinsurance)

    context = {
        'cusbuyinsurance': cusbuyinsurance,
        'msg': msg
    }
    return render(request, 'search_insurance.html', context=context)

# หน้ารายการกรมธรรม์พ.ร.บ.
@login_required
def comp_search(request):
    msg = ''
    searchcontractid = request.POST.get('contractid', '')
    searchlicense = request.POST.get('license', '')
    searchoname = request.POST.get('oname', '')
    searchosur = request.POST.get('osur', '')

    userid = request.user.id
    me = Person.objects.get(user_id=userid) #ตัวเรา=userที่ login
    takecare = Customer.objects.filter(seller_id=me.id) #ลูกค้าที่ userดูแล
    takecarelistid = []
    for i in takecare:
        takecarelistid.append(i.id)
    # takecarelistid คือ ไอดีลูกค้าที่ user ดูแล

    #กรมธรรม์ทั้งหมดของลูกค้าที่ user ดูแล และเพิ่ม7 วันล่าสุด
    cusbuycontract = Contract.objects.filter(customer_id__in=takecarelistid, register_date__gte=date.today() - timedelta(days=7))
    cusbuycontractlistid = [] 
    for i in cusbuycontract:
        cusbuycontractlistid.append(i) #ไอดีกรมธรรม์ทั้งหมดที่ลูกค้าที่ user ดูแล

    # print('ลูกค้าที่ซื้อพรบ')
    cusbuycoumpulsory = Compulsory_Insurance.objects.filter(contract_id__in=cusbuycontractlistid, contract__status='Available').order_by('-id')
    
    if request.method == 'POST':
        cusbuycontract = Contract.objects.filter(customer_id__in=takecarelistid)
        cusbuycontractlistid = [] 
        for i in cusbuycontract:
            cusbuycontractlistid.append(i) #ไอดีกรมธรรม์ทั้งหมดที่ลูกค้าที่ user ดูแล
        if 'search1' in request.POST and searchcontractid != '':
            cusbuycoumpulsory = Compulsory_Insurance.objects.filter(contract_id__in=cusbuycontractlistid, compulsory_id=searchcontractid)
            msg = 'ค้นหากรมธรรม์เลขที่ %s' %(searchcontractid)
        elif 'search2' in request.POST and searchoname != '' and searchosur != '' and searchlicense != '':
            cusbuycoumpulsory = Compulsory_Insurance.objects.filter(contract_id__in=cusbuycontractlistid, contract__car__license_on=searchlicense, contract__car__owner__fname=searchoname, contract__car__owner__lname=searchosur)
            msg = 'ค้นหากรมธรรม์ทะเบียนรถ %s ผู้เอาประกัน %s %s' %(searchlicense, searchoname, searchosur)

    context = {
        'cusbuycoumpulsory': cusbuycoumpulsory,
        'msg': msg
    }
    return render(request, 'search_compulsory.html', context=context)


# หน้าเปลี่ยนเลขทะเบียนรถจากกรมธรรม์
def change_license(request):
    provincelist = Province.objects.all()

    context = {
        'provincelist': provincelist
    }
    return render(request, 'change_license.html', context=context)


@csrf_exempt
def getcontract(request):
    data = json.loads(request.body)
    contractno = data['mycontract']
    contracttype = data['mytype']
    find = 'no'
    if contracttype == 'comp':
        try:
            comp = Compulsory_Insurance.objects.get(compulsory_id=contractno)
            car_license = comp.contract.car.license_on
            car_province = comp.contract.car.province_id
            find = 'yes'
        except Compulsory_Insurance.DoesNotExist:
            car_license = ''
            car_province = ''
    elif contracttype == 'ins':
        try:
            ins = Insurance_Policy.objects.get(insurance_id=contractno)
            car_license = ins.contract.car.license_on
            car_province = ins.contract.car.province_id
            find = 'yes'
        except Insurance_Policy.DoesNotExist:
            car_license = ''
            car_province = ''

    response = {
        'find': find,
        'car_license': car_license,
        'car_province': car_province
    }
    
    return JsonResponse(response, status=200)