# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-28 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_auto_20180428_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tests',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Test Name'),
        ),
    ]
