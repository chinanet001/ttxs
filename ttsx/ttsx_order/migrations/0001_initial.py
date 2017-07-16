# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttsx_goods', '0001_initial'),
        ('ttsx_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('goods', models.ForeignKey(to='ttsx_goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMain',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('order_id', models.CharField(max_length=20)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(max_digits=6, decimal_places=2)),
                ('state', models.IntegerField()),
                ('user', models.ForeignKey(to='ttsx_user.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(to='ttsx_order.OrderMain'),
        ),
    ]
