# Generated by Django 5.0.2 on 2024-10-11 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_wallet_userwallet'),
    ]

    operations = [
        migrations.DeleteModel(
            name='wallet',
        ),
    ]