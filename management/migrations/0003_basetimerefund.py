# Generated by Django 5.0.6 on 2024-06-11 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_car_license_plate'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTimeRefund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_time', models.PositiveIntegerField()),
            ],
        ),
    ]
