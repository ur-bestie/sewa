# Generated by Django 5.0.2 on 2024-11-12 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0011_housepicture_house'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='price',
            field=models.IntegerField(default=1000),
        ),
    ]