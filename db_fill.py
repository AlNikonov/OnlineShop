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
    orders = []
    for i in range(15):
        order = Order.objects.create(
            user_id = User.objects.get(id=random.randint(1,4)),
            status = Order.Status.DRAFT,
            address = fake.city(),
            #delivery_fee = 1.0
        )
        orders.append(order)
        print(f'Created order with id {order.order_id}, belongs to user {order.user_id}, address {order.address}')


    print('Show email of users which have orders with id in [2, 7, 9]')
    emails = User.objects.filter(order__order_id__in=[2,7,9]).values('email')
    print(emails)
handle()
