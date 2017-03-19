# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0002_urlvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='urlvalue',
            name='url',
            field=models.ForeignKey(to='search_engine.Url'),
        ),
    ]
