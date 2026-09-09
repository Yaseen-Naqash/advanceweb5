from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price','discount' , 'category', 'created_at', 'updated_at']
    search_fields = ['title']
    list_filter = ['category']

    pass


admin.site.register(Product, ProductAdmin)

admin.site.register(Category)