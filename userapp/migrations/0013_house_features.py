# Generated by Django 5.0.2 on 2024-11-12 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0012_house_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='features',
            field=models.TextField(default=1, max_length=10000),
            preserve_default=False,
        ),
    ]
