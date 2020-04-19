from django.urls import path
from . import views

urlpatterns = [
    path('search/insurance', views.ins_search, name="ins_search"),
    path('search/compulsory', views.comp_search, name='comp_search'),
]