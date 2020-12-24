# Generated by Django 3.1.4 on 2020-12-23 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialnetwork', '0016_auto_20201223_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='profile',
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default='', help_text='User submitted a post', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
