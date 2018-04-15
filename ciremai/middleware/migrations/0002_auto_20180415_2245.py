# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-15 15:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billing', '0003_auto_20180415_2235'),
        ('middleware', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instruments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
        ),
        migrations.CreateModel(
            name='OrderResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderresults_order', to='billing.Orders', verbose_name='Order')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeric_result', models.FloatField(null=True, verbose_name='Numeric result')),
                ('alfa_result', models.CharField(max_length=100, null=True, verbose_name='Alfanumeric result')),
                ('text_result', models.TextField(null=True, verbose_name='Text result')),
                ('image_result', models.BinaryField(null=True, verbose_name='Image result')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('instrument', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='results_instrument', to='middleware.Instruments', verbose_name='Instrument')),
                ('lastmodifiedby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='results_order', to='billing.Orders', verbose_name='Order')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='results_test', to='billing.Tests', verbose_name='Test')),
            ],
        ),
        migrations.AddField(
            model_name='orderresults',
            name='result',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orderresults_result', to='middleware.Results', verbose_name='Result'),
        ),
        migrations.AddField(
            model_name='orderresults',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderresults_test', to='billing.Tests', verbose_name='Test'),
        ),
    ]
