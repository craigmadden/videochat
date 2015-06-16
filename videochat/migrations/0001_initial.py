# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chatname', models.DateTimeField(auto_now_add=True)),
                ('chatend', models.DateTimeField(null=True)),
                ('chat_status', models.CharField(default=b'Active', max_length=10, choices=[(b'Active', b'Active'), (b'Waiting', b'Waiting'), (b'Terminated', b'Terminated')])),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('photo', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='contact',
            field=models.ForeignKey(related_name='chat', to='videochat.Contact', null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(related_name='chat', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
