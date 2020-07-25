# Generated by Django 3.0.8 on 2020-07-25 02:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, default='', max_length=280, verbose_name='Text')),
                ('slug', models.SlugField(default='', max_length=280, unique=True, verbose_name='Slug')),
                ('displayed', models.DateField(default=datetime.date(1970, 1, 1), verbose_name='Last Displayed')),
                ('tweeted', models.BooleanField(default=False, verbose_name='Tweeted')),
                ('votes', models.PositiveIntegerField(default=0, verbose_name='Votes')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, default='', max_length=340, verbose_name='Text')),
                ('slug', models.SlugField(default='', max_length=340, unique=True, verbose_name='Slug')),
            ],
        ),
    ]
