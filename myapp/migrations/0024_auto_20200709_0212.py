# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-09 01:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_auto_20200709_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='datetime',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Submission_datetime'),
        ),
    ]
