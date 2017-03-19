# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0004_auto_20160524_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlindex',
            name='words',
        ),
        migrations.RemoveField(
            model_name='wordcount',
            name='url',
        ),
        migrations.RemoveField(
            model_name='wordcount',
            name='word',
        ),
        migrations.DeleteModel(
            name='UrlIndex',
        ),
        migrations.DeleteModel(
            name='WordCount',
        ),
    ]
