from django.db import models

# Create your models here.
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
    

    def __str__(self):
        return self.title