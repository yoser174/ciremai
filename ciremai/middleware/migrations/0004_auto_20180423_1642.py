# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 09:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_auto_20180415_2235'),
        ('middleware', '0003_auto_20180423_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='order_test',
        ),
        migrations.AddField(
            model_name='results',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='results_order', to='billing.Orders', verbose_name='Order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='results',
            name='test',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='results_test', to='billing.Tests', verbose_name='Test'),
            preserve_default=False,
        ),
    ]
