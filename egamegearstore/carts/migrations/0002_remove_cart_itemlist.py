# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 09:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='itemList',
        ),
    ]
