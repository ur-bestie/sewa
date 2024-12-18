# Generated by Django 5.0.2 on 2024-12-13 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0047_tradeplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradeplan',
            name='balance',
        ),
        migrations.AddField(
            model_name='tradeplan',
            name='max',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=1000000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tradeplan',
            name='min',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=1000000),
            preserve_default=False,
        ),
    ]
