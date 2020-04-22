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

@login_required
# หน้ารายงานกรมธรรม์หมดอายุ
def ins_expire(request):

    userid = request.user.id
    me = Person.objects.get(user_id=userid) #ตัวเรา=userที่ login
    takecare = Customer.objects.filter(seller_id=me.id) #ลูกค้าที่ userดูแล
    takecarelistid = []
    for i in takecare:
        takecarelistid.append(i.id)
    # takecarelistid คือ ไอดีลูกค้าที่ user ดูแล

    #กรมธรรม์ทั้งหมดของลูกค้าที่ user ดูแล และเพิ่ม7 วันล่าสุด
    cusbuycontract = Contract.objects.filter(customer_id__in=takecarelistid, date_end_cover=date.today())
    cusbuycontractlistid = [] 
    for i in cusbuycontract:
        cusbuycontractlistid.append(i) #ไอดีกรมธรรม์ทั้งหมดของลูกค้าที่ user ดูแล

     # print('ลูกค้าที่ซื้อประกัน')
    cusbuyinsurance = Insurance_Policy.objects.filter(contract_id__in=cusbuycontractlistid, contract__status='Available').order_by('-id')

    context = {
        'cusbuyinsurance': cusbuyinsurance,
    }
    return render(request, 'ins_ex.html', context=context)

def comp_expire(request):
    return render(request, 'comp_ex.html')