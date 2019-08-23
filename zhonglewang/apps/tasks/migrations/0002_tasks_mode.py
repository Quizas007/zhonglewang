# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-20 02:01
from __future__ import unicode_literals

import apps.tasks.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='mode',
            field=models.IntegerField(choices=[(1, '自由模式'), (2, '担保模式')], default=1, validators=[apps.tasks.validator.valid_mode], verbose_name='模式'),
            preserve_default=False,
        ),
    ]