# Generated by Django 3.0.8 on 2020-08-15 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_about_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='title',
            field=models.CharField(default='', max_length=30, unique=True, verbose_name='Title'),
        ),
    ]
