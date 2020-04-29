from django.contrib import admin
from home.models import Car_Use_Type_Table, Person, Premium_Table, Company, Province, Brand
from contract.models import Customer, Owner, Car, Contract, Insurance_Policy, Compulsory_Insurance

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'card_id', 'phone', 'address', 'seller']
    list_filter = ['seller']
    search_fields = ['fname', 'lname', 'card_id', 'phone']
    list_per_page = 20

class OwnerAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'card_id', 'phone', 'address']
    search_fields = ['fname', 'lname', 'card_id', 'phone']
    list_per_page = 20

class CarAdmin(admin.ModelAdmin):
    list_display = ['license_on', 'date_register', 'province', 'brand', 'model', 'type', 'owner', 'chassis_on', 'displacement',
     'gvw', 'seat']

    fieldsets = [
        ('Car', {'fields': ['license_on', 'date_register', 'province', 'brand', 'model', 'type', 'owner']}),
        ('About', {'fields': ['displacement', 'gvw', 'seat'], 'classes': ['collapse']})
    ]

    list_filter = ['province', 'brand', 'model', 'type', 'owner']
    search_fields = ['license_on', 'province']
    list_per_page = 20

class ContractAdmin(admin.ModelAdmin):
    list_display = ['register_date', 'status', 'date_start_cover', 'date_end_cover', 'price', 'customer', 'company', 'car']
    list_filter = ['status', 'customer', 'company', 'car']
    list_per_page = 10

class Insurance_PolicyAdmin(admin.ModelAdmin):
    list_display = ['insurance_id', 'insurance_car_use_type', 'insurance_code', 'contract']
    list_filter = ['insurance_car_use_type', 'insurance_code']
    list_per_page = 20
    

class Compulsory_InsuranceAdmin(admin.ModelAdmin):
    list_display = ['compulsory_id', 'compulsory_car_use_type', 'contract']
    list_filter = ['compulsory_car_use_type']
    list_per_page = 20

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Insurance_Policy, Insurance_PolicyAdmin)
admin.site.register(Compulsory_Insurance, Compulsory_InsuranceAdmin)