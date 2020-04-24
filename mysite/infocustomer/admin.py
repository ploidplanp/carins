from django.contrib import admin
from infocustomer.models import Seller, Customer

# Register your models here.

admin.site.register(Customer)
class PriceInline(admin.TabularInline):
    model = Customer
    extra = 0

class CustomerAdmin(admin.ModelAdmin):
    inlines = [PriceInline]

admin.site.register(Seller)
class PriceInline(admin.TabularInline):
    model = Seller
    extra = 0

class FoodAdmin(admin.ModelAdmin):
    inlines = [PriceInline]
