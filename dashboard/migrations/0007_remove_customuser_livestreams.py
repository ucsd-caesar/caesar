# Generated by Django 4.2 on 2023-05-07 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_customuser_livestreams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='livestreams',
        ),
    ]
