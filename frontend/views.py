from django.shortcuts import render, redirect
from products.models import Products
from orders.models import Order, OrderProducts
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated



# Create your views here.

def login(request):
    context = {}
    return render(request, 'login.html', context)

def register(request):
    context = {}
    return render(request, 'registration.html', context)

def store(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'store.html', context)

def cart(request):
    refresh = request.COOKIES.get('refresh')
    print(refresh)
    token = RefreshToken(refresh)
    user = token['user_id']

    order = Order.objects.filter(user_id=user, status='DRAFT').first()
    products = OrderProducts.objects.filter(order_id=order)
    context = {'products':products}
    return render(request, 'cart.html', context)

@api_view(['GET'])
@login_required(login_url='/login')
def api_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    order = Order.objects.filter(user_id=request.user, status='DRAFT').first()
    products = OrderProducts.objects.filter(order_id=order)
    context = {'products':products, 'order':order}
    return render(request, 'cart.html', context)


def payment(request):
    context = {}
    return render(request, 'payment.html', context)

def user(request):
    context = {}
    return render(request, 'user.html', context)
