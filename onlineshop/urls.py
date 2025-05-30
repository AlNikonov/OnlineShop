"""
URL configuration for onlineshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from orders import views as order_views
from products import views as product_views
from users import views as user_views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from frontend import views as frontend_views

urlpatterns = [
    path('', frontend_views.store, name='store'),
    path('register', frontend_views.register, name='register'),
    path('login', frontend_views.login, name='login'),
    path('cart', frontend_views.api_cart, name='cart'),
    path('payment', frontend_views.payment, name='payment'),
    path('me', frontend_views.user, name='user'),


    path('admin/', admin.site.urls),
    path('update_item', order_views.update_item, name='update_item'),
    path('api/cart', order_views.cart, name='api_cart'),
    path('api/token/refresh', user_views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('orders/', order_views.get_orders, name='get_orders'),
    path('orders/<int:order_id>', order_views.order_details, name='order_details'),
    path('orders/create', order_views.create_order, name='create_order'),
    path('api/process_order', order_views.process_order, name='process_order'),
    path('products/', product_views.get_products, name='get_products'),
    path('products/<int:product_id>', product_views.product_details, name='product_details'),
    path('products/create', product_views.create_product, name='create_product'),
    path('users/', user_views.get_users, name='get_users'),
    path('auth/register', user_views.create_user, name='create_user'),
    path('auth/login', user_views.login, name='api_login'),
    path('api/change_password', user_views.change_password, name='change_password'),
    path('auth/logout', user_views.logout, name='api_logout'),
    path('api/user_info', user_views.user_details, name='user_details'),
    path('order_products', order_views.get_orders_details, name='get_orders_details'),
    path('orders/<int:order_id>/details', order_views.order_products_details, name='order_products_details'),
    path('order_products/create', order_views.create_order_product, name='create_order_product'),
]
