# Generated by Django 4.2.6 on 2023-11-03 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standard',
            old_name='maximum_speed',
            new_name='maximum_velocity',
        ),
        migrations.RenameField(
            model_name='standard',
            old_name='minimum_speed',
            new_name='minimum_velocity',
        ),
        migrations.RemoveField(
            model_name='standard',
            name='company',
        ),
    ]