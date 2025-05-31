from django.db import models

# Create your models here.
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    stored_amount = models.IntegerField(default=0)
    image = models.CharField(max_length=100, default='images/placeholder.png')
