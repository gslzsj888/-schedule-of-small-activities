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
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('pub_date', models.DateField(max_length=20)),
                ('time_start', models.CharField(max_length=20)),
                ('time_end', models.CharField(max_length=20)),
                ('release', models.DateField(auto_now=True)),
                ('introduce', models.TextField()),
                ('img', models.ImageField(upload_to=b'media/activity_pic/%Y-%m-%d')),
                ('cancered', models.IntegerField(default=0)),
                ('popular', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('checked', models.IntegerField(default=0)),
                ('overdue', models.IntegerField(default=0)),
                ('activity', models.ForeignKey(to='billboard.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=30)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subtitle', models.CharField(max_length=50)),
                ('brief', models.TextField()),
                ('tim', models.CharField(max_length=20)),
                ('activity', models.ForeignKey(related_name='stage', to='billboard.Activity')),
            ],
        ),
        migrations.AddField(
            model_name='agenda',
            name='user',
            field=models.ForeignKey(to='billboard.MyUser'),
        ),
        migrations.AddField(
            model_name='activity',
            name='builder',
            field=models.ForeignKey(to='billboard.MyUser'),
        ),
    ]
