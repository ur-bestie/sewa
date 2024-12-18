# Generated by Django 5.0.2 on 2024-11-25 20:10

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0019_houserentconfir'),
    ]

    operations = [
        migrations.CreateModel(
            name='withdraw_his',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('address', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('proof', models.FileField(upload_to='proof/')),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('paymentm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.paymentmethod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
