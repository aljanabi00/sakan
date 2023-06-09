# Generated by Django 4.2.1 on 2023-06-26 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_advertiser_package_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertiser',
            name='featured_limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advertiser',
            name='package_expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='advertiser',
            name='property_limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advertiser',
            name='property_period',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advertiser',
            name='repost_limit',
            field=models.IntegerField(default=0),
        ),
    ]
