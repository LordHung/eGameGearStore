# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 14:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_productfeatured_make_img_background'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productfeatured',
            old_name='make_img_background',
            new_name='make_image_background',
        ),
    ]