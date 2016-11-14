# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0004_remove_activity_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='release',
        ),
    ]
