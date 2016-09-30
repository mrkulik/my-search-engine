# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlValue',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('url', models.URLField()),
                ('word', models.ForeignKey(to='search_engine.Word')),
            ],
        ),
    ]
