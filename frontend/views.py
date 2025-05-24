from django.shortcuts import render




# Create your views here.

def testview(request):
    context = {}
    return render(request, 'test.html', context)

def register(request):
    context = {}
    return render(request, 'registration.html', context)

def store(request):
    context = {}
    return render(request, 'store.html', context)

def registration(request):
    context = {}
    return render(request, 'registration.html', context)


def cart(request):
    context = {}
    return render(request, 'cart.html', context)


def payment(request):
    context = {}
    return render(request, 'payment.html', context)
