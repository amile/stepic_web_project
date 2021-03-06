# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-18 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='added_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='added_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
