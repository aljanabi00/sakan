# Generated by Django 4.2.1 on 2023-06-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_advertiser_package_requested_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertiser',
            name='package_count',
            field=models.IntegerField(default=0),
        ),
    ]
