# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('videochat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chatstart',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='chat',
            name='chatname',
            field=models.CharField(max_length=50),
        ),
    ]
