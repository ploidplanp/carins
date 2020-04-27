from django.shortcuts import render, redirect
from infocustomer.models import Customer,Seller
from home.models import Company
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import Edit
from django.contrib.auth.decorators import login_required


# Create your views here.

def homepage(request, seller_id):
    print(seller_id)
    customer = get_customers_by_seller_id(seller_id)
    context = {
        'customer_name': customer      
    }
    return render(request, 'cusindex.html', context)

def get_customer():
    customer = Customer.objects.all()
    return customer

def get_customers_by_seller_id(seller_id):
    customers = Customer.objects.filter(seller_id = seller_id)
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
    print("Customer ID:", id)
    customer = Customer.objects.get(pk =id)
    return customer

@login_required
def edit_profile(request):
    context = {}
    if request.method == 'POST':
        form = Edit(request.POST)
        if request.user.is_authenticated:
            user = request.user
            seller_id = user.id
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
            return homepage(request, user.id)
    else:
        form = Edit(default_data, auto_id=False)
    return render(request, 'cusindex.html', {'form': form})

@login_required
def delete_profile(request, customer_id):
    if request.user.is_authenticated:
        user = request.user
        seller_id = user.id
    customer_obj = get_customer_id(customer_id)
    delete_customer(customer_obj)

    return redirect('/customer/' + str(seller_id))

@login_required
def Company_homepage(request):
    user = get_user_data()
    company = get_company_data()
    context = {
        'user_data' : user,
        'company_data' : company
    }
    return render(request, 'user.html', context)

def get_user_data():
    user = Seller.objects.all()
    return user

def get_company_data():
    company = Company.objects.all()
    return company

