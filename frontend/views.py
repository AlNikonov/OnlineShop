from django.shortcuts import render




# Create your views here.

def login(request):
    context = {}
    return render(request, 'login.html', context)

def register(request):
    context = {}
    return render(request, 'registration.html', context)

def store(request):
    context = {}
    return render(request, 'store.html', context)

def cart(request):
    context = {}
    return render(request, 'cart.html', context)

def payment(request):
    context = {}
    return render(request, 'payment.html', context)
