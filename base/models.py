from django.db import models
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
# Create your models here.


class Person(AbstractUser):
    phone = models.CharField(max_length=127, null=True, blank=True)
    GENDER = {  
        '0':'male',
        '1': 'femaie',
    }
    gender = models.CharField(max_length=1, choices=GENDER, null=True, default='0')
    external_id = models.CharField(max_length=127, null=True, blank=True)





class Category(models.Model):
    title = models.CharField(max_length=127, null=True)
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=127, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    image = models.ImageField(upload_to='images', null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def final_price(self):
        if self.discount:
            x = self.price - (self.price / 100 * self.discount)
            x = int(x)
            return x
        else:
            return self.price


    def __str__(self):
        return self.title