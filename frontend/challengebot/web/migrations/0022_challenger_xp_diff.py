# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0021_auto_20170802_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenger',
            name='xp_diff',
            field=models.IntegerField(default=0),
        ),
    ]
