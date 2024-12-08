# Generated by Django 5.0.2 on 2024-12-07 13:10

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0044_stock_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('current_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('running', models.BooleanField(default=False)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('Stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.stock')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]