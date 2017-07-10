# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('umail', models.CharField(max_length=20)),
                ('ushou', models.CharField(max_length=10, default='')),
                ('uaddress', models.CharField(max_length=100, default='')),
                ('ucode', models.CharField(max_length=6, default='')),
                ('uphone', models.CharField(max_length=11, default='')),
            ],
        ),
    ]
