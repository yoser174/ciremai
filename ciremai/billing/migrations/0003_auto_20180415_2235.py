# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-15 15:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billing', '0002_supergroups'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Insurence Name')),
                ('ext_code', models.CharField(max_length=30, verbose_name='External code')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Insurence',
                'verbose_name_plural': 'Insurences',
            },
        ),
        migrations.RemoveField(
            model_name='insurence',
            name='lastmodifiedby',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='insurence',
        ),
        migrations.AddField(
            model_name='testgroups',
            name='supergroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='testgroup_supergroup', to='billing.SuperGroups', verbose_name='Super Group'),
        ),
        migrations.AddField(
            model_name='tests',
            name='parent',
            field=models.IntegerField(help_text='Parent', null=True, verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='diagnosis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='billing.Diagnosis', verbose_name='Diagnosis'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='priority',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='billing.Priority', verbose_name='Order priority'),
        ),
        migrations.DeleteModel(
            name='Insurence',
        ),
        migrations.AddField(
            model_name='orders',
            name='insurance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='billing.Insurance', verbose_name='Insurance'),
        ),
    ]
