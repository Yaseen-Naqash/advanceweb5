from django.shortcuts import render, redirect
# Create your views here.


from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Property, Person, Attribute, City


def home(request):

    latest_properties = Property.objects.all().order_by('-created_at')[:3]



    context = {
        'latest_properties': latest_properties,

    }
    return render(request, 'index.html', context)


def properties(request):



    # price = request.GET.get('price',0)

    properties = Property.objects.all()


    
    


    cities = City.objects.all()
    attributes = Attribute.objects.all()
    context = {
        'properties':properties[:6],
        'types': Property.TYPE,
        'cities':cities,
        'attributes':attributes,
    }
    return render(request, 'deals.html', context)


def login_register(request):

    context = {
        
    }
    return render(request, 'login_register.html', context)