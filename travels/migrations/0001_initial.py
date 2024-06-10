# Generated by Django 5.0.6 on 2024-06-08 16:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('date_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('destanition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='d_travel', to='management.city')),
                ('driver_car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_car', to='management.drivercar')),
                ('startcity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_travel', to='management.city')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_available', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_ticket', to=settings.AUTH_USER_MODEL)),
                ('travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel_ticket', to='travels.travel')),
            ],
        ),
    ]
