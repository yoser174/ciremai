# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-06 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('middleware', '0009_auto_20180506_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='mark',
            field=models.CharField(max_length=3, null=True, verbose_name='Result mark'),
        ),
    ]