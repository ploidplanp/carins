from django.urls import path
from . import views

urlpatterns = [
    path('report/expire', views.report_expire, name='report_expire'),
    path('new/insurance', views.new_policy, name='new_policy'),
    path('new/compulsory', views.new_compulsory, name='new_compulsory'),
    path('search', views.contract_search, name="contract_search"),
    path('getowner/', views.getowner),
    path('getcar/', views.getcar),
    path('getcus/', views.getcus)
]