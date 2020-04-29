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
from contract.forms import ContractForm
# Create your views here.

# หน้าเปลี่ยนเลขทะเบียนรถจากกรมธรรม์
@login_required
def change_license(request):
    
    changeid = request.POST.get('contract_id', '')
    changetype = request.POST.get('contract_type', '')
    changenum = request.POST.get('new_license', '')
    changepro = request.POST.get('new_province', '')
    provincelist = Province.objects.all()
    if request.method == 'POST':
        if changetype == "ins":
            insurance = Insurance_Policy.objects.get(insurance_id = changeid)
            contract = Contract.objects.get(id = insurance.contract_id)
            car = Car.objects.get(id = contract.car_id)

            newcar = Car.objects.create(
                    license_on = changenum,
                    date_register = car.date_register,
                    province_id = changepro,
                    brand_id = car.brand_id,
                    model = car.model,
                    chassis_on = car.chassis_on,
                    displacement = car.displacement,
                    gvw = car.gvw,
                    seat = car.seat,
                    type = car.type,
                    owner_id = car.owner_id
            )

            contract.car_id = newcar.id
            contract.save()

        if changetype == "comp":
            compulsory = Compulsory_Insurance.objects.get(compulsory_id = changeid)
            contract = Contract.objects.get(id = compulsory.contract_id)
            car = Car.objects.get(id = contract.car_id)

            newcar = Car.objects.create(
                    license_on = changenum,
                    date_register = car.date_register,
                    province_id = changepro,
                    brand_id = car.brand_id,
                    model = car.model,
                    chassis_on = car.chassis_on,
                    displacement = car.displacement,
                    gvw = car.gvw,
                    seat = car.seat,
                    type = car.type,
                    owner_id = car.owner_id
            )

            contract.car_id = newcar.id
            contract.save()

    context = {
        'provincelist': provincelist
    }
    return render(request, 'change_license.html', context=context)

# หน้ารายการกรมธรรม์ประกัน
@login_required
def ins_search(request):
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

@login_required
def ins_edit(request, ins_id):
    userid = request.user.id
    me = Person.objects.get(user_id=userid) #ตัวเรา=userที่ login
    companylist = Company.objects.all()
    caruselist = Car_Use_Type_Table.objects.all().order_by('code')

    try:
        myins = Insurance_Policy.objects.get(id=ins_id)
    except Insurance_Policy.DoesNotExist:
        return redirect('ins_search')

    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data) # ทั้งก้อน
            
            try:
                owner = Owner.objects.get(card_id=form.cleaned_data['owner_cardid'])
                owner.card_id = form.cleaned_data['owner_cardid']
                owner.fname = form.cleaned_data['owner_fname']
                owner.lname = form.cleaned_data['owner_lname']
                owner.phone = form.cleaned_data['owner_phone']
                owner.address = form.cleaned_data['owner_address']
                owner.save()
            except Owner.DoesNotExist:
                owner = Owner.objects.create(
                    card_id = form.cleaned_data['owner_cardid'],
                    fname= form.cleaned_data['owner_fname'],
                    lname = form.cleaned_data['owner_lname'],
                    phone = form.cleaned_data['owner_phone'],
                    address = form.cleaned_data['owner_address'],
                )

            car = Car.objects.get(license_on=form.cleaned_data['car_license'], province=form.cleaned_data['car_province'], type=form.cleaned_data['car_type'])
            car.license_on = form.cleaned_data['car_license']
            car.date_register = form.cleaned_data['car_register']
            car.province_id = form.cleaned_data['car_province']
            car.brand_id = form.cleaned_data['car_brand']
            car.model = form.cleaned_data['car_model']
            car.chassis_on = form.cleaned_data['car_chassis']
            car.displacement = form.cleaned_data['car_displacement']
            car.gvw = form.cleaned_data['car_gvw']
            car.seat = form.cleaned_data['car_seat']
            car.type = form.cleaned_data['car_type']
            car.owner_id = owner.id
            car.save()

            try:
                cus = Customer.objects.get(fname=form.cleaned_data['cus_fname'], lname=form.cleaned_data['cus_lname'])
                cus.card_id = form.cleaned_data['cus_cardid']
                cus.fname = form.cleaned_data['cus_fname']
                cus.lname = form.cleaned_data['cus_lname']
                cus.phone = form.cleaned_data['cus_phone']
                cus.address = form.cleaned_data['cus_address']
                cus.seller_id = me.id
                cus.save()
            except Customer.DoesNotExist:
                cus = Customer.objects.create(
                    card_id = form.cleaned_data['cus_cardid'],
                    fname = form.cleaned_data['cus_fname'],
                    lname = form.cleaned_data['cus_lname'],
                    phone = form.cleaned_data['cus_phone'],
                    address = form.cleaned_data['cus_address'],
                    seller_id = me.id
                )

            if form.cleaned_data['contract_cover_end'] >= date.today():
                contract_status = 'Available'
            else:
                contract_status = 'Unavailable'

            myins.insurance_id = form.cleaned_data['contract_no']
            myins.insurance_code = request.POST.get('contractcodeSelect')
            myins.insurance_car_use_type_id = request.POST.get('caruseSelect')
            myins.save()

            mycon = Contract.objects.get(id=myins.contract_id)
            mycon.register_date = date.today()
            mycon.status = contract_status
            mycon.date_start_cover = form.cleaned_data['contract_cover_start']
            mycon.date_end_cover = form.cleaned_data['contract_cover_end']
            mycon.price = form.cleaned_data['contract_price']
            mycon.customer_id = cus.id
            mycon.company_id = request.POST.get('companySelect')
            mycon.save()

            return redirect('ins_search')
    else:
        form = ContractForm()

    context = {
        'form': form,
        'companylist': companylist,
        'caruselist': caruselist,
        'insid': ins_id,
        'myins': Insurance_Policy.objects.get(id=ins_id)
    }
    return render(request, 'edit_insurance.html', context=context)

@login_required
def comp_edit(request, comp_id):
    print(comp_id)
    userid = request.user.id
    me = Person.objects.get(user_id=userid) #ตัวเรา=userที่ login
    companylist = Company.objects.all()
    carpremium = Premium_Table.objects.all().order_by('code')

    try:
        mycomp = Compulsory_Insurance.objects.get(id=comp_id)
    except Compulsory_Insurance.DoesNotExist:
        return redirect('comp_search')

    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data) # ทั้งก้อน

            try:
                owner = Owner.objects.get(card_id=form.cleaned_data['owner_cardid'])
                owner.card_id = form.cleaned_data['owner_cardid']
                owner.fname = form.cleaned_data['owner_fname']
                owner.lname = form.cleaned_data['owner_lname']
                owner.phone = form.cleaned_data['owner_phone']
                owner.address = form.cleaned_data['owner_address']
                owner.save()
            except Owner.DoesNotExist:
                owner = Owner.objects.create(
                    card_id = form.cleaned_data['owner_cardid'],
                    fname= form.cleaned_data['owner_fname'],
                    lname = form.cleaned_data['owner_lname'],
                    phone = form.cleaned_data['owner_phone'],
                    address = form.cleaned_data['owner_address'],
                )

            car = Car.objects.get(license_on=form.cleaned_data['car_license'], province=form.cleaned_data['car_province'], type=form.cleaned_data['car_type'])
            car.license_on = form.cleaned_data['car_license']
            car.date_register = form.cleaned_data['car_register']
            car.province_id = form.cleaned_data['car_province']
            car.brand_id = form.cleaned_data['car_brand']
            car.model = form.cleaned_data['car_model']
            car.chassis_on = form.cleaned_data['car_chassis']
            car.displacement = form.cleaned_data['car_displacement']
            car.gvw = form.cleaned_data['car_gvw']
            car.seat = form.cleaned_data['car_seat']
            car.type = form.cleaned_data['car_type']
            car.owner_id = owner.id
            car.save()

            try:
                cus = Customer.objects.get(fname=form.cleaned_data['cus_fname'], lname=form.cleaned_data['cus_lname'])
                cus.card_id = form.cleaned_data['cus_cardid']
                cus.fname = form.cleaned_data['cus_fname']
                cus.lname = form.cleaned_data['cus_lname']
                cus.phone = form.cleaned_data['cus_phone']
                cus.address = form.cleaned_data['cus_address']
                cus.seller_id = me.id
                cus.save()
            except Customer.DoesNotExist:
                cus = Customer.objects.create(
                    card_id = form.cleaned_data['cus_cardid'],
                    fname = form.cleaned_data['cus_fname'],
                    lname = form.cleaned_data['cus_lname'],
                    phone = form.cleaned_data['cus_phone'],
                    address = form.cleaned_data['cus_address'],
                    seller_id = me.id
                )

            if form.cleaned_data['contract_cover_end'] >= date.today():
                contract_status = 'Available'
            else:
                contract_status = 'Unavailable'

            mycomp.compulsory_id = form.cleaned_data['contract_no']
            mycomp.compulsory_car_use_type_id = request.POST.get('caruseSelect')
            mycomp.save()

            mycon = Contract.objects.get(id=mycomp.contract_id)
            mycon.register_date = date.today()
            mycon.status = contract_status
            mycon.date_start_cover = form.cleaned_data['contract_cover_start']
            mycon.date_end_cover = form.cleaned_data['contract_cover_end']
            mycon.price = form.cleaned_data['contract_price']
            mycon.customer_id = cus.id
            mycon.company_id = request.POST.get('companySelect')
            mycon.save()

            

            return redirect('comp_search')
    else:
        form = ContractForm()

    context = {
        'form': form,
        'companylist': companylist,
        'carpremium': carpremium,
        'compid': comp_id,
        'mycomp': Compulsory_Insurance.objects.get(id=comp_id)
    }
    return render(request, 'edit_compulsory.html', context=context)

@login_required
def ins_delete(request, ins_id):
    myins = Insurance_Policy.objects.get(id=ins_id)
    mycon = Contract.objects.get(id=myins.contract_id)
    myins.delete()
    mycon.delete()
    return redirect('ins_search')

@login_required
def comp_delete(request, comp_id):
    mycomp = Compulsory_Insurance.objects.get(id=comp_id)
    mycon = Contract.objects.get(id=mycomp.contract_id)
    mycomp.delete()
    mycon.delete()
    return redirect('comp_search')

#ใช้สำหรับหน้าเปลี่ยนเลขทะเบียนรถ
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

@csrf_exempt
def getins(request):
    data = json.loads(request.body)
    insid = data['insid']
    myins = Insurance_Policy.objects.get(id=insid)
    own = myins.contract.car.owner
    car = myins.contract.car
    cus = myins.contract.customer
    
    response = {
        'insurance_id': myins.insurance_id,
        'own_cardid': own.card_id,
        'own_fname': own.fname,
        'own_lname': own.lname,
        'own_phone': own.phone,
        'own_address': own.address,
        'car_license': car.license_on,
        'car_province': car.province.id,
        'car_type': car.type,
        'car_regist': car.date_register,
        'car_brand': car.brand.id,
        'car_model': car.model,
        'car_chassis': car.chassis_on,
        'car_displacement': car.displacement,
        'car_gvw': car.gvw,
        'car_seat': car.seat,
        'contract_code': myins.insurance_code,
        'contract_sdate': myins.contract.date_start_cover,
        'contract_edate': myins.contract.date_end_cover,
        'contract_price': myins.contract.price,
        'cus_fname': cus.fname,
        'cus_lname': cus.lname,
        'cus_phone': cus.phone,
        'cus_address': cus.address,
        'cus_cardid': cus.card_id
    }

    return JsonResponse(response, status=200)

@csrf_exempt
def getcomp(request):
    data = json.loads(request.body)
    compid = data['compid']
    mycomp = Compulsory_Insurance.objects.get(id=compid)
    own = mycomp.contract.car.owner
    car = mycomp.contract.car
    cus = mycomp.contract.customer

    response = {
        'compulsory_id': mycomp.compulsory_id,
        'own_cardid': own.card_id,
        'own_fname': own.fname,
        'own_lname': own.lname,
        'own_phone': own.phone,
        'own_address': own.address,
        'car_license': car.license_on,
        'car_province': car.province.id,
        'car_type': car.type,
        'car_regist': car.date_register,
        'car_brand': car.brand.id,
        'car_model': car.model,
        'car_chassis': car.chassis_on,
        'car_displacement': car.displacement,
        'car_gvw': car.gvw,
        'car_seat': car.seat,
        'contract_sdate': mycomp.contract.date_start_cover,
        'contract_edate': mycomp.contract.date_end_cover,
        'contract_price': mycomp.contract.price,
        'cus_fname': cus.fname,
        'cus_lname': cus.lname,
        'cus_phone': cus.phone,
        'cus_address': cus.address,
        'cus_cardid': cus.card_id
    }

    return JsonResponse(response, status=200)