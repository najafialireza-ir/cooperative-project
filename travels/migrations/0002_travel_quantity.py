# Generated by Django 5.0.6 on 2024-06-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]