# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 16:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20170307_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-title']},
        ),
    ]