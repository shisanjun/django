# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-30 01:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_userprofile_stu_account'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('can_access_my_course', '我的课程'),), 'verbose_name': '用户信息', 'verbose_name_plural': '用户信息'},
        ),
    ]
