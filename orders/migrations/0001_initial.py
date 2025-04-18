# Generated by Django 5.2 on 2025-04-18 19:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('DRAFT', 'Черновик'), ('PROCESS', 'В процессе'), ('COMPLETE', 'Выполнен')], default='DRAFT')),
                ('address', models.CharField(max_length=256, null=True)),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('amount', models.IntegerField(default=1)),
                ('pk', models.CompositePrimaryKey('product_id', 'order_id', blank=True, editable=False, primary_key=True, serialize=False)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
            ],
        ),
    ]
