# Generated by Django 5.0.6 on 2024-06-03 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transectionlog',
            name='transection_type',
            field=models.CharField(choices=[('1', 'request'), ('2', 'order')], max_length=10, null=True),
        ),
    ]