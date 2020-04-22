from django.urls import path
from . import views

urlpatterns = [
    path('ins_expire', views.ins_expire, name='ins_expire'),
    path('comp_expire', views.comp_expire, name='comp_expire')
]