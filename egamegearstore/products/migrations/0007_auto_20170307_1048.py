# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 10:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20170306_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
    ]
