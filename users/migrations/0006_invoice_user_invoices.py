# Generated by Django 4.2.1 on 2023-05-22 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_package_remove_accounttype_property_limit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.package')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='invoices',
            field=models.ManyToManyField(blank=True, to='users.invoice'),
        ),
    ]
