# Generated by Django 4.2 on 2023-05-24 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('dashboard', '0014_livestream_latest_frame'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livestream',
            name='groups',
            field=models.ManyToManyField(default=None, related_name='livestreams', to='auth.group'),
        ),
    ]
