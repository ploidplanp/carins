from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import PROTECT


# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=PROTECT, null=True)
    card_id = models.CharField(max_length=13)
    phone = models.CharField(max_length=10)
    
    def __str__(self):
        return '%s %s (%s)' %(self.user.first_name, self.user.last_name, self.phone)

class Car_Use_Type_Table(models.Model):
    code = models.CharField(max_length=3)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s : %s' %(self.code, self.info)

class Premium_Table(models.Model):
    code = models.CharField(max_length=5)
    make_model = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    premium = models.FloatField(default=0.00)
    revenue_stamp = models.FloatField(default=0.00)
    vat = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)

    def __str__(self):
        return '%s : %s' %(self.code, self.make_model)

class Company(models.Model):
    name = models.CharField(max_length=255)
    tax_no = models.CharField(max_length=13)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=10)
    picture = models.CharField(max_length=255, default= 'https://i.stack.imgur.com/l60Hf.png')

    def __str__(self):
        return '%s' %self.name

class Province(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '%s' %self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return '%s' %self.name