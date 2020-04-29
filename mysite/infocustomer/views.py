from django.shortcuts import render, redirect
from home.models import Company, Person
from contract.models import Customer
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import Edit, EditUser, EditCompany
from django.contrib.auth.decorators import login_required


# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        user = request.user
        person_id = user.id
    customer = get_customers_by_person_id(person_id)
    context = {
        'customer_name': customer      
    }
    return render(request, 'managecus.html', context)

def get_customer():
    customer = Customer.objects.all()
    return customer

def get_customers_by_person_id(person_id):
    customers = Customer.objects.filter(seller_id = person_id)
    return customers
 

def delete_customer(customer_obj):
    customer_obj.delete()
    
@login_required
def edit_cus_page(request, customer_id):
    customer_data = get_customer_id(customer_id)
    default_data = {'cardid': customer_data.card_id, 'phone': customer_data.phone, 'address': customer_data.address}
    form = Edit(default_data, auto_id=False)
    context = {
        'customer_id': customer_id,
        'customer_data': customer_data,
        'form': form
    }
    return render(request, 'editcus.html', context)

def get_customer_id(id):
    customer = Customer.objects.get(pk = id)
    return customer

@login_required
def edit_profile(request):
    context = {}
    if request.method == 'POST':
        form = Edit(request.POST)
        if request.user.is_authenticated:
            user = request.user
            person_id = user.id
            print("i love sky")
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
        form = Edit(default_data, auto_id=False)
    return render(request, 'managecus.html', {'form': form})

@login_required
def delete_profile(request, customer_id):
    print("--> Delete customer")
    if request.user.is_authenticated:
        user = request.user
        seller_id = user.id
    customer_obj = get_customer_id(customer_id)
    delete_customer(customer_obj)

    return redirect('/customer/')

@login_required
def User_homepage(request):
    user = get_user_data()
    context = {
        'user_data' : user,
    }
    return render(request, 'manageuser.html', context)

@login_required
def Company_homepage(request):
    company = get_company_data()
    context = {
        'company_data' : company
    }
    return render(request, 'managecompany.html', context)
def get_user_data():
    user = Person.objects.all()
    return user

def get_user_by_id(id):
    user = Person.objects.get(pk = id)
    return user

def get_company_data():
    company = Company.objects.all()
    return company

def get_company_by_id(id):
    company = Company.objects.get(pk = id)
    return company

def User_info(request):
    user = get_user_data()
    context = {
        'user_data' : user,
    }
    return render(request, 'user.html', context)

def edit_user_page(request, user_id):
    user_data = get_user_by_id(user_id)
    default_data = {'cardid': user_data.card_id, 'phone': user_data.phone}
    form = EditUser(default_data, auto_id=False)
    context = {
        'user_id': user_id,
        'user_data': user_data,
        'form': form
    }
    return render(request, 'edituser.html', context)

@login_required
def edit_user_profile(request):
    context = {}
    print("AAAAAA")
    if request.method == 'POST':
        form = EditUser(request.POST)
        print("xxxxx")
        if request.user.is_authenticated:
            user = request.user
            print("i love sky")
            if form.is_valid():  
                print("Form is valid")
                card_id = form.cleaned_data['cardid']
                phone = form.cleaned_data['phone']
                Person_to_edit_id =  request.POST.get('id')  

                user_obj = get_user_by_id(Person_to_edit_id)
                print(user_obj)       
                user_obj.card_id = card_id
                user_obj.phone = phone
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


def edit_company_page(request, company_id):
    company_data = get_company_by_id(company_id)
    default_data = {'taxno': company_data.tax_no, 'phone': company_data.phone, 'address': company_data.phone}
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
    print("AAAAAA")
    if request.method == 'POST':
        form = EditCompany(request.POST)
        print("xxxxx")
        if request.user.is_authenticated:
            user = request.user
            print("i love sky")
            if form.is_valid():  
                print("Form is valid")
                taxno = form.cleaned_data['taxno']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                company_to_edit_id =  request.POST.get('id')  

                company_obj = get_company_by_id(company_to_edit_id)
                print(company_obj)       
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
    if request.user.is_authenticated:
        user = request.user
    company_obj = get_company_by_id(company_id)
    delete_company(company_obj)

    return redirect('/managecompany/')

def delete_company(company_obj):
    company_obj.delete()

def add_customer_page(request):
    result = get_user_object()
    context = {
        'user_all': result
    }
    print(request)
    return render(request, 'addcus.html', context)

def add_customer_submit(request):
    userid = request.user.id
    me = Person.objects.get(user_id=userid)
    if request.method == 'POST':
        print("naruk")
        cus = Customer.objects.create(
            card_id =  request.POST.get('card_id'),
            fname = request.POST.get('Fname'),
            lname = request.POST.get('Lname'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address'),
            seller_id = me.id,
            picture = request.POST.get('picture')
        )
        return homepage(request)

def get_user_object():
    result = User.objects.all()
    return result


