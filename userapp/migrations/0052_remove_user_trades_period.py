# Generated by Django 5.0.2 on 2024-12-13 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0051_user_trades_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_trades',
            name='period',
        ),
    ]