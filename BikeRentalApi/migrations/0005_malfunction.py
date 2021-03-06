# Generated by Django 3.1.7 on 2021-05-04 20:51

import BikeRentalApi.enums
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BikeRentalApi', '0004_remove_rental_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Malfunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('state', django_enumfield.db.fields.EnumField(default=1, enum=BikeRentalApi.enums.MalfunctionState)),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BikeRentalApi.bike')),
                ('reporting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
