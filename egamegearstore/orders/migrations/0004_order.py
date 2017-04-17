# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_cart_tax_percentage'),
        ('orders', '0003_useraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billing_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='orders.UserAddress')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='orders.UserAddress')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.UserCheckout')),
            ],
        ),
    ]