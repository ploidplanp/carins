import json
from datetime import date

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

from .forms import ContractForm


# Create your views here.


@login_required
# หน้าเพิ่มกรมธรรม์ ประกัน
def new_policy(request):
    userid = request.user.id
    me = Person.objects.get(user_id=userid) #ตัวเรา=userที่ login
    companylist = Company.objects.all()
    caruselist = Car_Use_Type_Table.objects.all().order_by('code')
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data) # ทั้งก้อน
            print('-----------')

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
            # myowner = Owner.objects.get(card_id=form.cleaned_data['owner_cardid'])

            try:
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
            except Car.DoesNotExist:
                car = Car.objects.create(
                    license_on = form.cleaned_data['car_license'],
                    date_register = form.cleaned_data['car_register'],
                    province_id = form.cleaned_data['car_province'],
                    brand_id = form.cleaned_data['car_brand'],
                    model = form.cleaned_data['car_model'],
                    chassis_on = form.cleaned_data['car_chassis'],
                    displacement = form.cleaned_data['car_displacement'],
                    gvw = form.cleaned_data['car_gvw'],
                    seat = form.cleaned_data['car_seat'],
                    type = form.cleaned_data['car_type'],
                    owner_id = owner.id
                )
            # mycar = Car.objects.get(license_on=form.cleaned_data['car_license'], province=form.cleaned_data['car_province'], type=form.cleaned_data['car_type'])

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
            # mycus = Customer.objects.get(fname=form.cleaned_data['cus_fname'], lname=form.cleaned_data['cus_lname'])

            if form.cleaned_data['contract_cover_end'] >= date.today():
                contract_status = 'Available'
            else:
                contract_status = 'Unavailable'
            
            contract = Contract.objects.create(
                register_date = date.today(),
                status = contract_status,
                date_start_cover = form.cleaned_data['contract_cover_start'],
                date_end_cover = form.cleaned_data['contract_cover_end'],
                price = form.cleaned_data['contract_price'],
                customer_id = cus.id,
                company_id = request.POST.get('companySelect'),
                car_id = car.id
            )
            lastcontract = Contract.objects.latest('id')

            newins = Insurance_Policy.objects.create(
                insurance_id = form.cleaned_data['contract_insid'],
                insurance_car_use_type_id = request.POST.get('caruseSelect'),
                insurance_code = request.POST.get('contractcodeSelect'),
                contract_id = lastcontract.id
            )
            return redirect('ins_search')
    else:
        form = ContractForm()

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

# -----------------