from django.urls import path
from . import views

urlpatterns = [
    path('report/expire', views.report_expire, name='report_expire')
]