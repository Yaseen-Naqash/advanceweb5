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


class Property(models.Model):
    TYPE = [
        ('0','آپارتمان'),
        ('1','ویلا'),
        ('1','تجاری'),
        ('1','اداری'),
        ('1','زمین'),

    ]

    DEAL_TYPE = [
        ('0','خرید'),
        ('1','اجاره'),

    ]
    title = models.CharField(max_length=127, null=True, blank=True)
    rooms = models.CharField(max_length=127, null=True, blank=True)
    parking = models.BooleanField(max_length=127, null=True, blank=True)
    backyard = models.CharField(max_length=127, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    type = models.CharField(max_length=1, choices=TYPE, null=True, blank=True)
    deal_type = models.CharField(max_length=1, choices=DEAL_TYPE, null=True, blank=True)
    Attributes = models.ManyToManyField('Attribute')

    created_at = models.DateTimeField(auto_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    city = models.ForeignKey('City', null=True, blank=True)


    def __str__(self):

        return self.title


class Attribute(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)
    is_included = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.title

class City(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)

    def __str__(self):
        return self.title
