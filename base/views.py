from django.shortcuts import render, redirect
# Create your views here.


from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Property, Person, Attribute, City

from django.core.paginator import Paginator


def home(request):

    latest_properties = Property.objects.all().order_by('-created_at')[:3]



    context = {
        'latest_properties': latest_properties,

    }
    return render(request, 'index.html', context)


def properties(request):

    # from django.core.paginator import Paginator

    all_properties = Property.objects.all()

    x = Paginator(all_properties, 9)

    properties = x.get_page(request.GET.get('page',1))


    
    


    cities = City.objects.all()
    attributes = Attribute.objects.all()
    context = {
        'properties':properties,
        'types': Property.TYPE,
        'cities':cities,
        'attributes':attributes,
    }
    return render(request, 'deals.html', context)


def login_register(request):

    if request.method == 'POST':

        if request.POST.get('type') == 'login':
            pass

        else:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1==password2:

                x = Person.objects.create(
                    first_name = name,
                    phone=phone,
                    username=username,
                    email=email,
                    password=password2

                )
                x.set_password(password2)
                x.save()
                return redirect('home_url')
            else:
                messages.error(request,'bluh bluh bluh')
                return redirect('login_register_url')





    context = {
        
    }
    return render(request, 'login_register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login_register_url')