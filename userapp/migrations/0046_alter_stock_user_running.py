# Generated by Django 5.0.2 on 2024-12-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0045_stock_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock_user',
            name='running',
            field=models.BooleanField(default=True),
        ),
    ]