from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('company/', views.company_detail, name='company_detail'),
    path('car-use-type/', views.cartype_detail, name='cartype_detail'),
    path('premium-table/', views.premium_detail, name='premium_detail'),
    path('mycustomer/', views.mycustomer, name='mycustomer'),
]