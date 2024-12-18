# Generated by Django 5.0.2 on 2024-12-16 18:44

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0055_stocks_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='compStocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('stocks_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.stocks_plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
