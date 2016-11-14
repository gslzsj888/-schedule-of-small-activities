# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0005_remove_activity_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='release',
            field=models.DateField(default=datetime.datetime(2016, 11, 14, 18, 25, 54, 793255, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
