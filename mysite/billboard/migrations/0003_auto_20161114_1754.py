# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0002_auto_20161114_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='img',
            field=models.ImageField(null=True, upload_to=b'activitypic/%Y/%m/%d', blank=True),
        ),
    ]
