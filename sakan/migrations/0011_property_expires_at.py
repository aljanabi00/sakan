# Generated by Django 4.2.1 on 2023-06-26 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sakan', '0010_offer_en_name_propertytype_en_name_province_en_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
