# Generated by Django 4.2 on 2023-05-07 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_admin',
            new_name='is_staff',
        ),
    ]
