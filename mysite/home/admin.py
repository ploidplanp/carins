from codecs import register

from django.contrib import admin

from home.models import Car_Use_Type_Table, Person, Premium_Table

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'phone', 'username']

class Car_Use_Type_TableAdmin(admin.ModelAdmin):
    list_display = ['code', 'info']
    search_fields = ['code', 'info']

class Premium_TableAdmin(admin.ModelAdmin):
    list_display = ['code', 'make_model', 'info']

admin.site.register(Person, PersonAdmin)
admin.site.register(Car_Use_Type_Table, Car_Use_Type_TableAdmin)
admin.site.register(Premium_Table, Premium_TableAdmin)
