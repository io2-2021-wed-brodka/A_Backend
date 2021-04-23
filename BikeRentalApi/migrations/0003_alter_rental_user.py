# Generated by Django 3.2 on 2021-04-23 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BikeRentalApi', '0002_admin_appuser_rental_tech'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BikeRentalApi.person'),
        ),
    ]