# Generated by Django 5.0.2 on 2024-12-03 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0043_rename_last_update_stock_ldate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='image',
            field=models.FileField(default=1, upload_to='stocks/'),
            preserve_default=False,
        ),
    ]
