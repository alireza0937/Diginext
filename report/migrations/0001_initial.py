# Generated by Django 4.2.6 on 2023-11-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('st_id', models.IntegerField()),
                ('timestamp', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'CarLocations',
                'db_table': 'CarLocations',
            },
        ),
    ]
