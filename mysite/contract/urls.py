from django.urls import path
from . import views

urlpatterns = [
    path('report/expire', views.report_expire, name='report_expire'),
    path('new/insurance', views.new_policy, name='new_policy'),
    path('new/compulsory', views.new_compulsory, name='new_compulsory'),
    path('search/insurance', views.ins_search, name="ins_search"),
    path('search/compulsory', views.comp_search, name='comp_search'),
    path('getowner/', views.getowner),
    path('getcar/', views.getcar),
    path('getcus/', views.getcus)
]