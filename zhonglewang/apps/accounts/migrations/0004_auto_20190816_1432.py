# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-16 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_avator'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='qq',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='QQ号'),
        ),
        migrations.AddField(
            model_name='user',
            name='realname',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='真实姓名'),
        ),
    ]
