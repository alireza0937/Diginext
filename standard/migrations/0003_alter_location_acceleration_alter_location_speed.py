# Generated by Django 4.2.6 on 2023-11-22 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='acceleration',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='location',
            name='speed',
            field=models.FloatField(),
        ),
    ]