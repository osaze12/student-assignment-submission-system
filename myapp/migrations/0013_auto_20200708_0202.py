# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-08 01:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20200708_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf_file',
            name='gradd',
            field=models.CharField(default='No Grade yet', max_length=3),
        ),
    ]
