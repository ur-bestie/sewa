# Generated by Django 5.0.2 on 2024-12-01 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0038_housepicture_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
