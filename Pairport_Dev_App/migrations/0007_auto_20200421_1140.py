# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-04-21 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pairport_Dev_App', '0006_auto_20200421_0458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_details',
            name='image_five',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='image_four',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='image_one',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='image_three',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='image_two',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='job',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='moto',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='residence_country',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='travel_country',
        ),
    ]
