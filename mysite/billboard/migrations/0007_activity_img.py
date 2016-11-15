# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0006_activity_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='img',
            field=models.ImageField(null=True, upload_to=b'activitypic/%Y/%m/%d', blank=True),
        ),
    ]
