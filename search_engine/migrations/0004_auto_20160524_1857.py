# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0003_auto_20160523_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='text',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
