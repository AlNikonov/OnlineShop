import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlineshop.settings")
django.setup()

from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User

from users.models import User
from products.models import Products
from orders.models import Order, OrderProducts

from faker import Faker
import random


def fill_users_table():
    fake = Faker()
    users = []
    for i in range(5):
        user = User.objects.create(
            email=fake.ascii_free_email(),
            password=fake.password(length=10),
            username=fake.name(),
        )
        users.append(user)
        print(
            f'Created user with email {user.email}, password {user.password}, username {user.username}')


def fill_orders_table():
    fake = Faker()
    orders = []
    for i in range(15):
        order = Order.objects.create(
            user_id=User.objects.get(id=random.randint(1, 4)),
            status=Order.Status.DRAFT,
            address=fake.city(),
            delivery_fee=1.0
        )
        orders.append(order)
        print(f'Created order with id {order.order_id}, belongs to user {order.user_id}, address {order.address}')


def fill_products_table():
    fake = Faker()
    products = []
    for i in range(20):
        product = Products.objects.create(
            product_name=fake.word(),
            price=random.randint(10, 100),
            stored_amount=random.randint(1, 10),
        )
        products.append(product)
        print(
            f'Create product {product.product_name} with id {product.product_id}, price {product.price}, stored {product.stored_amount}')


def fill_order_products_table():
    fake = Faker()
    order_products = []
    for i in range(30):
        order_product = OrderProducts.objects.create(
            order_id=Order.objects.get(order_id=max(int(i / 2), 1)),
            product_id=Products.objects.get(product_id=random.randint(1, 20)),
            amount=random.randint(1, 15)
        )
        order_products.append(order_product)
        print(f'Added {order_product.amount} products {order_product.product_id} to {order_product.order_id}')


def handle():
    print('Show email of users which have orders with id in [2, 7, 9]')
    emails = User.objects.filter(order__order_id__in=[2, 7, 9]).values('email')
    print(emails)

    print('Show products ordered by user')
    orders = Order.objects.filter(user_id=1)
    for order in orders:
        print(f'Order: {order.order_id}')
        order_products = OrderProducts.objects.filter(order_id=order)
        for product in order_products:
            name = product.product_id.product_name
            amount = product.amount
            print(f'Product {name}, amount: {amount}')

def create_single_product():
    product = Products.objects.create(
        product_name = 'Product',
        price = 100,
        stored_amount = 4,
        #image = 'images/404placeholder.jpg'
    )

#create_single_product()
fill_users_table()
fill_products_table()
fill_orders_table()
fill_order_products_table()
#handle()