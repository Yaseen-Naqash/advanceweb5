from django.shortcuts import render, redirect
# Create your views here.


from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Property, Person, Attribute


def home(request):

    latest_properties = Property.objects.all().order_by('-created_at')[:3]



    context = {
        'latest_properties': latest_properties,

    }
    return render(request, 'index.html', context)


def properties(request):

    q = request.GET.get('q','')
    city = request.GET.get('city','')
    type = request.GET.get('type','')
    
    properties = Property.objects.all()



    context = {
        'properties':properties,
    }
    return render(request, 'deals.html', context)


def login_register(request):

    context = {
        
    }
    return render(request, 'login_register.html', context)