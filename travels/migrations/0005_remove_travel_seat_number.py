# Generated by Django 5.0.6 on 2024-06-10 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0004_travel_seat_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel',
            name='seat_number',
        ),
    ]
