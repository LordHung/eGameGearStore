# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercheckout',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]