# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 03:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wl_app', '0006_auto_20171022_2358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='join',
            name='user',
        ),
        migrations.RemoveField(
            model_name='join',
            name='wish',
        ),
        migrations.RemoveField(
            model_name='wish',
            name='wisher',
        ),
        migrations.DeleteModel(
            name='Join',
        ),
        migrations.DeleteModel(
            name='Wish',
        ),
    ]
