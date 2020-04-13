from builtins import license

from django.db import models

from home.models import (Brand, Car_Use_Type_Table, Company, Person,
                         Premium_Table, Province)

inscode_choice = (
    ('a', '1'), ('b', '2'), ('c', '3'), ('d', '3+')
)

status_choice = (
    ('av', 'available'), ('uv', 'unavailable')
)
type_choice = (
    ('a', 'รถยนต์'), ('b', 'จักรยานยนต์')
)

# Create your models here.
class Customer(models.Model):
    card_id = models.CharField(max_length=13)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)
    seller = models.ForeignKey(Person, on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s' %(self.fname, self.lname)

class Owner(models.Model):
    card_id = models.CharField(max_length=13)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s %s' %(self.fname, self.lname)

class Car(models.Model):
    license_on = models.CharField(max_length=7)
    date_register = models.DateField(auto_now=False, auto_now_add=False)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    model = models.CharField(max_length=255)
    chassis_on = models.CharField(max_length=17)
    displacement = models.IntegerField()
    gvw = models.IntegerField()
    seat = models.IntegerField()
    type = models.CharField(max_length=12, choices=type_choice)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)

    def __str__(self):
        return '%s (%s)' %(self.license_on, self.province)

class Contract(models.Model):
    register_date = models.DateField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=11, choices=status_choice)
    date_start_cover = models.DateField(auto_now=False, auto_now_add=False)
    date_end_cover = models.DateField(auto_now=False, auto_now_add=False)
    price = models.FloatField(default=0.00)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s (%s until %s)' %(self.car, self.car.owner, self.date_start_cover, self.date_end_cover)

class Insurance_Policy(models.Model):
    insurance_id = models.CharField(max_length=50)
    insurance_car_use_type = models.ForeignKey(Car_Use_Type_Table, on_delete=models.PROTECT)
    insurance_code = models.CharField(max_length=2, choices=inscode_choice)
    #
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)

class Compulsory_Insurance(models.Model):
    compulsory_id = models.CharField(max_length=50)
    compulsory_car_use_type = models.ForeignKey(Premium_Table, on_delete=models.PROTECT)
    #
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)
