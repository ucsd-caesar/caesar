# Generated by Django 4.2 on 2023-05-23 23:31

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('dashboard', '0012_livestream_hls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livestream',
            name='agency',
        ),
        migrations.RemoveField(
            model_name='livestream',
            name='hls',
        ),
        migrations.AddField(
            model_name='livestream',
            name='groups',
            field=models.ManyToManyField(default=builtins.any, related_name='livestreams', to='auth.group'),
        ),
        migrations.AddField(
            model_name='livestream',
            name='type',
            field=models.CharField(default='rtsp', max_length=255),
        ),
    ]