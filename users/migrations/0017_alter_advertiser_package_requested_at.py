# Generated by Django 4.2.1 on 2023-06-25 16:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_advertiser_package_requested_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertiser',
            name='package_requested_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
