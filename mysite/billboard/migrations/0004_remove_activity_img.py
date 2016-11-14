# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0003_auto_20161114_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='img',
        ),
    ]
