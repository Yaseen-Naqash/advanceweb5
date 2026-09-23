from django.shortcuts import render, redirect
from .models import Product, Category, Person
# Create your views here.


from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


def detail(request, pk):

    product = Product.objects.get(id=pk)
    context = {
        'product' : product
    }
    return render(request, 'detail.html', context)

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('home_url')
        else:
            messages.error(request, 'username or password is incorrect')
            return redirect('login_url')

    return render(request, 'login.html')



def register(request):


    
    if request.method == 'POST':
        x = Person.objects.create(
            username='saDasdasdasd',
            password='asdasdasd',
            email='asdasda',
            first_name='asdasdasd',
            last_name='asdasdasd',
        )

        x.set_password('asdasdasd'),






    return render(request, 'login.html')

