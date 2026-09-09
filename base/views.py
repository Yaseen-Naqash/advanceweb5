from django.shortcuts import render
from .models import Product
# Create your views here.
def home(request):
    products = Product.objects.all()




    context = {
        'products':products,
        'test':'test',
    }

    return render(request, 'django-template.html', context)