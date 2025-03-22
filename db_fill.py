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


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker()

        users = []
        for i in range(5):
            user = User.objects.create(
                login=fake.first_name(),
                email=fake.ascii_free_email(),
                password=fake.password(length=10),
                username=fake.name(),
            )
            users.append(user)
            print(f'Created user with login {user.login}, email {user.email}, password {user.password}, username {user.username}')

        products = []
        for i in range(5):
            product = Products.objects.create(
                product_name = fake.city(),
                price = i * 10,
                stored_amount = i * 5,
            )
            products.append(product)
            print(f'Created product with name {product.product_name}, price {product.price}, stored amount {product.stored_amount}')