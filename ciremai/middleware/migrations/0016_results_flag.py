# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 14:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('middleware', '0015_instruments_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='flag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='results_instrumentflag', to='middleware.InstrumentFlags', verbose_name='Instrument flag'),
        ),
    ]
