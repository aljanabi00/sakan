# Generated by Django 4.2.1 on 2023-07-04 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sakan', '0013_alter_statistic_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
