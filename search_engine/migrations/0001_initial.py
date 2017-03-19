# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UrlIndex',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WordCount',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('url', models.ForeignKey(to='search_engine.UrlIndex')),
                ('word', models.ForeignKey(to='search_engine.Word')),
            ],
        ),
        migrations.AddField(
            model_name='urlindex',
            name='words',
            field=models.ManyToManyField(to='search_engine.Word'),
        ),
    ]
