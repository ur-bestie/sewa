# Generated by Django 5.0.2 on 2024-11-29 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0032_user_shares_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_shares',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
