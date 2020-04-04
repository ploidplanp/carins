from django.db import models

# Create your models here.
# class person(models.Model):
#     card_id = models.CharField(max_length=13)
#     fname = models.CharField(max_length=255)
#     lname = models.CharField(max_length=255)
#     phone = models.CharField(max_length=10)
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)

# class car_use_type_table(models.Model):
#     code = models.CharField(max_length=3)
#     info = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return '%s : %s' %(self.code, self.info)

# class premium_table(models.Model):
#     code = models.CharField(max_length=5)
#     make_model = models.CharField(max_length=25)
#     info = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return '%s : %s' %(self.code, self.make_model)