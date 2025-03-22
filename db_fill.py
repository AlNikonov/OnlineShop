import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlineshop.settings")
django.setup()

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from users.models import User
from products.models import Products, ProductImages
from orders.models import Order, OrderProducts

from faker import Faker
import random



def handle():
    fake = Faker()

    '''users = []
    for i in range(5):
        user = User.objects.create(
            login=fake.first_name(),
            email=fake.ascii_free_email(),
            password=fake.password(length=10),
            username=fake.name(),
        )
        users.append(user)
        print(f'Created user with login {user.login}, email {user.email}, password {user.password}, username {user.username}')
'''
    '''orders = []
    for i in range(15):
        order = Order.objects.create(
            user_id = User.objects.get(id=random.randint(1,4)),
            status = Order.Status.DRAFT,
            address = fake.city(),
            #delivery_fee = 1.0
        )
        orders.append(order)
        print(f'Created order with id {order.order_id}, belongs to user {order.user_id}, address {order.address}')'''

    products = []
    for i in range(20):
        product = Products.objects.create(
            product_name=fake.city(),
            price=random.randint(10, 100),
            stored_amount=random.randint(1, 10),
        )
        products.append(product)
        print(f'Create product {product.product_name} with id {product.product_id}, price {product.price}, stored {product.stored_amount}')

    order_products = []
    for i in range (30):
        order_product = OrderProducts.objects.create(
            order_id = Order.objects.get(id=i/2),
            product_id = Products.objects.get(product_id=random.randint(1, 20)),
            amount = random.randint(1, 15)
        )
        order_products.append(order_product)
        print(f'Added {order_product.amount} products {order_product.product_id} to {order_product.order_id}')

    print('Show email of users which have orders with id in [2, 7, 9]')
    emails = User.objects.filter(order__order_id__in=[2,7,9]).values('email')
    print(emails)

    print('Show order products grouped by user')
    user = User.objects.get(id=1)
    ords = Order.objects.filter(user_id=1)
    order_info = []
    for order in ords:

        order_products = OrderProducts.objects.filter(order_id=ords)

        products_in_order = []
        for product in order_products:
            products_in_order.append([product.product_id, product.amount])
        order_info.append([order.order_id, products_in_order])
    print(f'User with id {1} have orders:')
    for order in order_info:
        print(f'order id {order[0]}, contains products wwith id\'s {order[1][0]}')
handle()
