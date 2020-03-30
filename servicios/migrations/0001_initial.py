# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-31 18:12
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeguridadJefeHijo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notificacion', models.BooleanField(default=False)),
                ('jefe_seguridad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguridad_jefe_servicio_jefe', to='usuarios.Perfil')),
                ('pariente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguridad_jefe_servicio_pariente', to='usuarios.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='SeguridadServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guardia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kilometraje', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('velocidad', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('telefono', models.CharField(max_length=15)),
                ('frecuencia_rastreo', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil')),
            ],
        ),
        migrations.AddField(
            model_name='seguridadservicio',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicios.Servicio'),
        ),
        migrations.AlterUniqueTogether(
            name='seguridadservicio',
            unique_together=set([('servicio', 'guardia')]),
        ),
        migrations.AlterUniqueTogether(
            name='seguridadjefehijo',
            unique_together=set([('pariente', 'jefe_seguridad')]),
        ),
    ]
