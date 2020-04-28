from django.contrib import admin
from infocustomer.models import Seller
from contract.models import Customer

# Register your models here.


admin.site.register(Seller)
class PriceInline(admin.TabularInline):
    model = Seller
    extra = 0

class FoodAdmin(admin.ModelAdmin):
    inlines = [PriceInline]
