# Generated by Django 4.2.1 on 2023-05-26 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_package_can_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
