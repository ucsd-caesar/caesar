# Generated by Django 4.2 on 2023-05-19 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_alter_customuser_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='livestream',
            name='hls',
            field=models.URLField(blank=True, null=True),
        ),
    ]