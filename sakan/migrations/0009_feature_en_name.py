# Generated by Django 4.2.1 on 2023-06-16 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sakan', '0008_propertytype_province_property_area_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='en_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
