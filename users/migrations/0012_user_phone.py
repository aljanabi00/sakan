# Generated by Django 4.2.1 on 2023-06-02 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_user_email_remove_user_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
