# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0007_activity_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='img',
            field=models.ImageField(null=True, upload_to=b'media/activitypic/%Y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='release',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
