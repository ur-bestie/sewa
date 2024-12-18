# Generated by Django 5.0.2 on 2024-10-11 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_remove_userwallet_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='paymentmethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('walletaddress', models.CharField(max_length=100)),
                ('logo', models.FileField(upload_to='pimage/')),
                ('pinfo', models.TextField(max_length=100)),
            ],
        ),
    ]
