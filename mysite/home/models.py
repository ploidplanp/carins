from django.db import models

# Create your models here.
class Person(models.Model):
    card_id = models.CharField(max_length=13)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Car_Use_Type_Table(models.Model):
    code = models.CharField(max_length=3)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s : %s' %(self.code, self.info)

class Premium_Table(models.Model):
    code = models.CharField(max_length=5)
    make_model = models.CharField(max_length=25)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s : %s' %(self.code, self.make_model)

class Company(models.Model):
    name = models.CharField(max_length=255)
    tax_no = models.CharField(max_length=13)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=10)

class Province(models.Model):
    name = models.CharField(max_length=255)

class Brand(models.Model):
    name = models.CharField(max_length=255)