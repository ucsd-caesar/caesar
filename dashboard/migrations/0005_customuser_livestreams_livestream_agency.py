# Generated by Django 4.2 on 2023-05-07 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_livestream_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='livestreams',
            field=models.ManyToManyField(related_name='livestreams', to='dashboard.livestream'),
        ),
        migrations.AddField(
            model_name='livestream',
            name='agency',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='livestreams', to='dashboard.agency'),
        ),
    ]
