# Generated by Django 3.1.4 on 2020-12-23 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0013_auto_20201223_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='nickname',
        ),
    ]
