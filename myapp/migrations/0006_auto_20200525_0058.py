# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-24 23:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20200525_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='pd',
        ),
        migrations.RemoveField(
            model_name='pdf_file',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
