# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-28 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20180223_1511'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='host',
            options={'verbose_name': '主机信息', 'verbose_name_plural': '主机信息'},
        ),
        migrations.AlterModelOptions(
            name='hostgroup',
            options={'verbose_name': '主机组', 'verbose_name_plural': '主机组'},
        ),
        migrations.AlterModelOptions(
            name='idc',
            options={'verbose_name': '机房', 'verbose_name_plural': '机房'},
        ),
        migrations.AlterModelOptions(
            name='remoteuser',
            options={'verbose_name': '主机用户', 'verbose_name_plural': '主机用户'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '系统用户', 'verbose_name_plural': '系统用户'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bind_group',
            field=models.ManyToManyField(blank=True, to='repository.HostGroup', verbose_name='主机组'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bind_host',
            field=models.ManyToManyField(blank=True, to='repository.BindHosts', verbose_name='主机'),
        ),
    ]
