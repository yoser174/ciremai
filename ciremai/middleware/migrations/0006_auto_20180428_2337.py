# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-28 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('middleware', '0005_auto_20180428_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrefranges',
            name='age_from',
            field=models.IntegerField(blank=True, null=True, verbose_name='Age from'),
        ),
        migrations.AlterField(
            model_name='testrefranges',
            name='age_to',
            field=models.IntegerField(blank=True, null=True, verbose_name='Age to'),
        ),
        migrations.AlterField(
            model_name='testrefranges',
            name='age_type',
            field=models.CharField(blank=True, choices=[('D', 'DAY'), ('M', 'MONTH'), ('Y', 'YEAR')], max_length=3, null=True, verbose_name='Age to unit'),
        ),
        migrations.AlterField(
            model_name='testrefranges',
            name='alfa_value',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Alfanumberic value'),
        ),
        migrations.AlterField(
            model_name='testrefranges',
            name='gender',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='refranges_gender', to='billing.Genders', verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='testrefranges',
            name='lower',
            field=models.IntegerField(blank=True, null=True, verbose_name='lower limit'),
        ),
        migrations.AlterField(
            model_name='testrefranges',
            name='operator',
            field=models.IntegerField(blank=True, null=True, verbose_name='operator value'),
        ),
        migrations.AlterField(
            model_name='testrefranges',
            name='special_info',
            field=models.TextField(blank=True, null=True, verbose_name='Special information'),
        ),
        migrations.AlterField(
            model_name='testrefranges',
            name='upper',
            field=models.IntegerField(blank=True, null=True, verbose_name='upper limit'),
        ),
    ]