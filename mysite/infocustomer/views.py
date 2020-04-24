from django.shortcuts import render, redirect
from infocustomer.models import Customer,Seller,Company
from django.http import HttpResponseRedirect

# Create your views here.

def homepage(request, seller_id):
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
    

def editpage(request, customer_id):
    customer_data = get_customer_id(customer_id)
    context = {
        'customer_id': customer_id,
        'customer_data': customer_data
    }
    return render(request, 'edit.html', context)

def get_customer_id(id):
    customer = Customer.objects.get(pk =id)
    return customer

def edit_profile(request):
    context = {}
    if request.method == 'POST':
        card_id = request.POST.get('cardid')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        cus_id =  request.POST.get('id')

        customer_obj = get_customer_id(cus_id)           
        customer_obj.card_id = card_id
        customer_obj.phone = phone
        customer_obj.address = address
        customer_obj.save()          

    return homepage(request)

def delete_profile(request, customer_id):
    customer_obj = get_customer_id(customer_id)
    delete_customer(customer_obj)

    return redirect('/customer/')


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


