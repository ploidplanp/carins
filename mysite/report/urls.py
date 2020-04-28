from django.urls import path
from . import views

urlpatterns = [
    path('ins_expire', views.ins_expire, name='ins_expire'),
    path('ins_expire/report/<str:check>/', views.ins_expire_report, name='ins_expire_report'),
    path('comp_expire', views.comp_expire, name='comp_expire'),
    path('comp_expire/report/<str:check>/', views.comp_expire_report, name='comp_expire_report')
]