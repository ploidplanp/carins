from django.urls import path
from . import views

urlpatterns = [
    path('new/insurance', views.new_policy, name='new_policy'),
    path('new/compulsory', views.new_compulsory, name='new_compulsory'),
    path('new/customer', views.add_customer, name='add_customer')
]