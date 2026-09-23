from django.shortcuts import render
from .models import Product, Category
# Create your views here.


def home(request):

    # products = Product.objects.all()


    # if request.GET.get('q') is not None:
    #     q = request.GET.get('q')
    # else:
    #     q=''
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    products = Product.objects.all() if q=='' else Product.objects.filter(title__icontains=q)

    if request.GET.get('category') is not None:
        products = products.filter(category__title=request.GET.get('category'))

    categories = Category.objects.all()

    

    context = {
        'products':products,
        'categories': categories,
    }

    return render(request, 'django-template.html', context)


def account(request):

    return render(request, 'account.html')


def detail(request):

    return render(request, '')
