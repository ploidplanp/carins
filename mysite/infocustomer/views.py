from django.shortcuts import render, redirect
from home.models import Company, Person
from contract.models import Customer
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import EditCus, EditUser, EditCompany
from django.contrib.auth.decorators import login_required


# Create your views here.

#Customer_homeage หน้าดูข้อมูลลูกค้า 
def homepage(request):
    if request.user.is_authenticated:
        user = request.user
        person_id = user.id
    customer = get_customers_by_person_id(person_id)
    context = {
        'customer_name': customer      
    }
    return render(request, 'managecus.html', context)
# -------------------------------------------------------


def get_customer():
    customer = Customer.objects.all()
    return customer

def get_customers_by_person_id(person_id):
    customers = Customer.objects.filter(seller_id = person_id)
    return customers
 

def get_customer_id(id):
    customer = Customer.objects.get(pk = id)
    return customer

#หน้า Edit Customer 
@login_required
def edit_cus_page(request, customer_id):
    customer_data = get_customer_id(customer_id)
    default_data = {'cardid': customer_data.card_id, 'phone': customer_data.phone, 'address': customer_data.address}
    form = EditCus(default_data, auto_id=False)
    context = {
        'customer_id': customer_id,
        'customer_data': customer_data,
        'form': form
    }
    return render(request, 'editcus.html', context)

#กด submit ในหน้า edit พอกดเสร็จให้ไปโผล่หน้า แสดงข้อมูลcustomer
@login_required
def edit_cus_profile(request):
    context = {}
    if request.method == 'POST':
        form = EditCus(request.POST)
        if request.user.is_authenticated:
            user = request.user
            person_id = user.id
            if form.is_valid():  
                card_id = form.cleaned_data['cardid']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                cus_id =  request.POST.get('id')  

                customer_obj = get_customer_id(cus_id)           
                customer_obj.card_id = card_id
                customer_obj.phone = phone
                customer_obj.address = address
                customer_obj.save() 
            return homepage(request)
    else:
        form = EditCus(default_data, auto_id=False)
    return render(request, 'managecus.html', {'form': form})

#delete customer
@login_required
def delete_cus_profile(request, customer_id):
    print("--> Delete customer")
    customer_obj = get_customer_id(customer_id)
    delete_customer(customer_obj)

    return redirect('/customer/')

def delete_customer(customer_obj):
    customer_obj.delete()

def add_customer_page(request):
    context = {

    }

    return render(request, 'addcus.html', context)

def add_customer_submit(request):
    userid = request.user.id
    # me = Person.objects.get(user_id=userid)
    if request.method == 'POST':
        cus = Customer.objects.create(
            card_id =  request.POST.get('card_id'),
            fname = request.POST.get('Fname'),
            lname = request.POST.get('Lname'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address'),
            seller_id = userid,
            picture = request.POST.get('picture')
        )
        return homepage(request)


# ---------------------------------------------------------

@login_required
def User_homepage(request):
    person = get_user_data()
    user = User.objects.all()
    context = {
        'person_data' : person,
        'user_data': user
    }
    return render(request, 'manageuser.html', context)

def get_user_data():
    user = Person.objects.all()
    return user

def get_user_by_id(id):
    user = Person.objects.get(pk = id)
    return user

def User_info(request):
    user = get_user_data()
    context = {
        'user_data' : user,
    }
    return render(request, 'user.html', context)

def edit_user_page(request, user_id):
    person_data = get_user_by_id(user_id)
    user_data = User.objects.get(pk = user_id)
    default_data = {'cardid': person_data.card_id, 'phone': person_data.phone, 'email': user_data.email}
    form = EditUser(default_data, auto_id=False)
    context = {
        'user_id': user_id,
        'user_data': person_data,
        'form': form
    }
    return render(request, 'edituser.html', context)

@login_required
def edit_user_profile(request):
    context = {}
    if request.method == 'POST':
        form = EditUser(request.POST)
        if request.user.is_authenticated:
            user = request.user
            if form.is_valid():  
                print("Form is valid")
                card_id = form.cleaned_data['cardid']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']
                Person_to_edit_id =  request.POST.get('id')  

                person_obj = get_user_by_id(Person_to_edit_id)
                user_obj = User.objects.get(pk = Person_to_edit_id)

                user_obj.email = email

                person_obj.card_id = card_id
                person_obj.phone = phone

                person_obj.save() 
                user_obj.save()
            return User_homepage(request)
    else:
        form = EditUser(default_data, auto_id=False)
    return render(request, 'manageuser.html', {'form': form})


@login_required
def delete_user_profile(request, person_id):
    person_obj = get_user_by_id(person_id)
    user_obj = User.objects.get(pk = person_id)
    delete_user(person_obj)
    delete_user(user_obj)

    return redirect('/manageuser/')

def delete_user(user_obj):
    user_obj.delete()

def add_user_page(request):
    result = get_user_data()
    context = {

    }
    return render(request, 'adduser.html', context)

def add_user_submit(request):
    userid = request.user.id
    me = Person.objects.get(user_id=userid)
    if request.method == 'POST':
        user = User.objects.create(
            username = request.POST.get('username'),
            password = request.POST.get('password'),
            first_name = request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            email = request.POST.get('email'),
            
        )
        person = Person.objects.create(
            id = user.id,
            card_id = request.POST.get('card_id'),
            phone = request.POST.get('phone'),
            picture = request.POST.get('picture'),
            user_id = user.id,         
        )
        return User_homepage(request)


# Company
@login_required
def Company_homepage(request):
    company = get_company_data()
    context = {
        'company_data' : company
    }
    return render(request, 'managecompany.html', context)

def get_company_data():
    company = Company.objects.all()
    return company

def get_company_by_id(id):
    company = Company.objects.get(pk = id)
    return company


def edit_company_page(request, company_id):
    company_data = get_company_by_id(company_id)
    default_data = {'taxno': company_data.tax_no, 'phone': company_data.phone, 'address': company_data.address}
    form = EditCompany(default_data, auto_id=False)
    context = {
        'company_id': company_id,
        'company_data': company_data,
        'form': form
    }
    return render(request, 'editcompany.html', context)

@login_required
def edit_company_profile(request):
    context = {}
    if request.method == 'POST':
        form = EditCompany(request.POST)
        if request.user.is_authenticated:
            user = request.user
            if form.is_valid():  
                
                taxno = form.cleaned_data['taxno']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                company_to_edit_id =  request.POST.get('id')  

                company_obj = get_company_by_id(company_to_edit_id)      
                company_obj.tax_no = taxno
                company_obj.phone = phone
                company_obj.address = address
                company_obj.save() 
            return Company_homepage(request)
    else:
        form = EditCompany(default_data, auto_id=False)
    return render(request, 'managecompany.html', {'form': form})

@login_required
def delete_company_profile(request, company_id):
    company_obj = get_company_by_id(company_id)
    delete_company(company_obj)

    return redirect('/managecompany/')

def delete_company(company_obj):
    company_obj.delete()

def add_company_page(request):
    result = get_company_data()
    context = {

    }
    return render(request, 'addcom.html', context)

def add_company_submit(request):
    userid = request.user.id
    me = Person.objects.get(user_id=userid)
    if request.method == 'POST':
        com = Company.objects.create(
            name = request.POST.get('name'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address'),
            picture = request.POST.get('picture')
        )
        return Company_homepage(request)



def get_user_object():
    result = User.objects.all()
    return result



