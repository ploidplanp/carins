from codecs import register

from django.contrib import admin

from home.models import Car_Use_Type_Table, Person, Premium_Table, Company, Province, Brand

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_id', 'phone']

class Car_Use_Type_TableAdmin(admin.ModelAdmin):
    list_display = ['code', 'info']
    search_fields = ['code', 'info']

class Premium_TableAdmin(admin.ModelAdmin):
    list_display = ['code', 'make_model', 'info']

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_no', 'address', 'phone']

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Person, PersonAdmin)
admin.site.register(Car_Use_Type_Table, Car_Use_Type_TableAdmin)
admin.site.register(Premium_Table, Premium_TableAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Brand, BrandAdmin)
