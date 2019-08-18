# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-16 04:59
from __future__ import unicode_literals

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190803_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avator',
            field=easy_thumbnails.fields.ThumbnailerImageField(default='avator/default.jpg', upload_to='avator/%Y%m%d/', verbose_name='头像'),
        ),
    ]
