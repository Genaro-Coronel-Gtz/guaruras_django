# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-07 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_perfil_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
