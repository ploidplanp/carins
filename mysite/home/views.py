from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.contrib.auth import authenticate, login, logout

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

    return render(request, template_name='login.html')

def mylogout(request):
    logout(request)
    print('logout')
    return redirect('mylogin')

# กดที่ home
def profile(request):
    return render(request, 'profile.html')

# กดที่ ดูข้อมูล เลือก บริษัท จะแสดงรายชื่อบริษัททั้งหมด
def company_detail(request):
    return render(request, 'company.html')

# กดที่ ดูข้อมูล เลือก ตารางอัตราเบี้ยพ.ร.บ.
def premium_detail(request):
    return render(request, 'premiumTable.html')

# กดที่ ดูข้อมูล เลือก ตารางรหัสการใช้รถ
def cartype_detail(request):
    return render(request, 'carUseType.html')
