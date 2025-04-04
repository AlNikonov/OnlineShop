from django.db import models
from users.models import User
from products.models import Products
# Create your models here.
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        PROCESS = 'PROCESS', 'В процессе'
        COMPLETE = 'COMPLETE', 'Выполнен'

    status = models.CharField(choices=Status.choices, default=Status.DRAFT)

    address = models.CharField(max_length=256, null=True)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)

class OrderProducts(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    pk = models.CompositePrimaryKey("product_id", "order_id")

