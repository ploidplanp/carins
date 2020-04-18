from builtins import object

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.views.decorators.csrf import csrf_exempt

from home.models import Car_Use_Type_Table, Company, Person, Premium_Table

# Create your views here.

def mylogin(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('profile')
            # return render(request, template_name='home.html')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'something wrong, please try again :\')'

    return render(request, template_name='login.html', context=context)

def mylogout(request):
    logout(request)
    print('logout')
    return redirect('mylogin')

# กดที่ home
@login_required
def profile(request):
    print(request.user)
    print(request.user.id)
    profile = Person.objects.filter(user=request.user)
    print(profile)
    
    context = {
        'profile': profile
    }
    return render(request, 'profile.html', context=context)

# กดที่ ดูข้อมูล เลือก บริษัท จะแสดงรายชื่อบริษัททั้งหมด
@login_required
def company_detail(request):
    table = Company.objects.all().order_by('id')

    context = {
        'table': table
    }
    return render(request, 'company.html', context=context)

# กดที่ ดูข้อมูล เลือก ตารางอัตราเบี้ยพ.ร.บ.
@login_required
def premium_detail(request):
    table = Premium_Table.objects.all().order_by('code')

    context = {
        'table': table
    }
    return render(request, 'premiumTable.html', context=context)

# กดที่ ดูข้อมูล เลือก ตารางรหัสการใช้รถ
@login_required
def cartype_detail(request):
    table = Car_Use_Type_Table.objects.all().order_by('code')

    context = {
        'table': table
    }
    return render(request, 'carUseType.html', context=context)
