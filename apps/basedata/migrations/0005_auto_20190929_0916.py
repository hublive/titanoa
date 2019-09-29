# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-09-29 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0004_auto_20190928_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='p_endtime',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='领取时间'),
        ),
        migrations.AlterField(
            model_name='property',
            name='p_image',
            field=models.ImageField(blank=True, default='image/default.png', null=True, upload_to='property/%Y-%m-%d', verbose_name='资产图片'),
        ),
    ]
