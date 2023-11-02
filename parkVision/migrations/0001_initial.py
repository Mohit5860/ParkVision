# Generated by Django 3.2.22 on 2023-10-25 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_number', models.CharField(max_length=30)),
                ('slot_number', models.IntegerField()),
                ('time', models.TimeField()),
            ],
        ),
    ]
