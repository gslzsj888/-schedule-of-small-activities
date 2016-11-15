# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='img',
            field=models.ImageField(upload_to=b'media/activitypic/%Y-%m-%d'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
