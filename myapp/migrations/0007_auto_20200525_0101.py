# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-25 00:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20200525_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdf_file',
            name='student',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.DeleteModel(
            name='Pdf_file',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]