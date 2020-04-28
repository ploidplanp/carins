from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from home.models import Company, Person

# Create your models here.

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=PROTECT, null=True)
    card_id = models.CharField(max_length=13)
    phone =  models.CharField(max_length=10)
    picture = models.CharField(max_length=255, default= 'https://i.stack.imgur.com/l60Hf.png')

    def __str__(self):
        return '%s %s (%s)' %(self.user.first_name, self.user.last_name, self.phone)
    


