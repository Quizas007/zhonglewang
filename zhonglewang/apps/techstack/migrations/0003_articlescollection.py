# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-14 08:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('techstack', '0002_auto_20190812_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlesCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='收藏/取消时间')),
                ('status', models.BooleanField(default=True, verbose_name='收藏状态')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles_collection_set', to='techstack.Articles', verbose_name='文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles_collection_set', to=settings.AUTH_USER_MODEL, verbose_name='收藏者')),
            ],
            options={
                'verbose_name': '收藏记录',
                'verbose_name_plural': '收藏记录',
            },
        ),
    ]
