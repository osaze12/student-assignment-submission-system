# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-09 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_remove_pdf_file_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='datetime',
        ),
        migrations.AddField(
            model_name='teacher',
            name='from_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='to_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Submission_datetime',
        ),
    ]