"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from home import views as home_views
from infocustomer import views as customer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.mylogin, name='mylogin'),
    path('logout', home_views.mylogout, name='mylogout'),
    path('home/', include('home.urls')),
    path('contract/', include('contract.urls')),
    path('customer/', customer_views.homepage, name='cusindex'),
    path('edit_cus/<customer_id>/', customer_views.edit_cus_page),
    path('customers/', customer_views.edit_profile ,name='edit_page'),
    path('delete/<customer_id>/', customer_views.delete_profile ,name='delete_customer'),
    path('user/', customer_views.User_info, name='userindex'),
    path('managecompany/', customer_views.Company_homepage, name='companyindex'),
    path('manageuser/', customer_views.User_homepage, name='userindex'),
    path('report/', include('report.urls')),
    path('contractinfo/', include('contractinfo.urls')),
    path('edit_user/<user_id>/', customer_views.edit_user_page),
    path('manageusers/', customer_views.edit_user_profile ,name='edit_user_page'),
    path('deleteuser/<person_id>/', customer_views.delete_user_profile ,name='delete_user'),
    path('edit_company/<company_id>/', customer_views.edit_company_page),
    path('managecompanys/', customer_views.edit_company_profile ,name='edit_company_page'),
    path('deletecompany/<company_id>/', customer_views.delete_company_profile ,name='delete_company'),
    path('addcustomer/',customer_views.add_customer_page),
    path('managecustomers/',customer_views.add_customer_submit, name='add_cus'),
]
