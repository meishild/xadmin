# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-18 05:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_host_administrator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='administrator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'Admin'),
        ),
    ]
