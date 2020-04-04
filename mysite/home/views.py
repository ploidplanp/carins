from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.context_processors import request

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
    return render(request, 'profile.html')

# กดที่ ดูข้อมูล เลือก บริษัท จะแสดงรายชื่อบริษัททั้งหมด
@login_required
def company_detail(request):
    return render(request, 'company.html')

# กดที่ ดูข้อมูล เลือก ตารางอัตราเบี้ยพ.ร.บ.
@login_required
def premium_detail(request):
    return render(request, 'premiumTable.html')

# กดที่ ดูข้อมูล เลือก ตารางรหัสการใช้รถ
@login_required
def cartype_detail(request):
    return render(request, 'carUseType.html')
