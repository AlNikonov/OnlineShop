# Generated by Django 5.2 on 2025-04-02 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_delivery_fee_orderproducts_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproducts',
            name='pk',
            field=models.CompositePrimaryKey('product_id', 'order_id', blank=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orderproducts',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]
