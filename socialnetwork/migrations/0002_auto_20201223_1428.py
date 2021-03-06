# Generated by Django 3.1.4 on 2020-12-23 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.TextField(default='', verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.TextField(default='', unique=True, verbose_name='Nickname'),
        ),
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.TextField(default='', verbose_name='Surname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='e_mail',
            field=models.EmailField(default='', max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', verbose_name='Post content')),
                ('user_id', models.ForeignKey(help_text='User submitted a post', on_delete=django.db.models.deletion.CASCADE, to='socialnetwork.user', verbose_name='User')),
            ],
        ),
    ]
