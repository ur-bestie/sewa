# Generated by Django 5.0.2 on 2024-12-18 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0057_compstocks_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compstocks',
            name='current_price',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
        migrations.AlterField(
            model_name='stock',
            name='current_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50),
        ),
        migrations.AlterField(
            model_name='stock',
            name='initial_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50),
        ),
        migrations.AlterField(
            model_name='stock_user',
            name='current_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50),
        ),
        migrations.AlterField(
            model_name='stock_user',
            name='initial_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=50),
        ),
        migrations.AlterField(
            model_name='stocks_plan',
            name='current_price',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
        migrations.AlterField(
            model_name='tradeplan',
            name='max',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
        migrations.AlterField(
            model_name='tradeplan',
            name='min',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
    ]