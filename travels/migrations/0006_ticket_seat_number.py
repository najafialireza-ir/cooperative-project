# Generated by Django 5.0.6 on 2024-06-10 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0005_remove_travel_seat_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='seat_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]