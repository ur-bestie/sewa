# Generated by Django 5.0.2 on 2024-11-29 14:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0027_shares_img_user_shares_shares'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_shares',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
