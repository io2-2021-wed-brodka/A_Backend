# Generated by Django 3.1.7 on 2021-03-31 09:11

import BikeRentalApi.enums
from django.db import migrations
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('BikeRentalApi', '0002_user_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='role',
            field=django_enumfield.db.fields.EnumField(default=0, enum=BikeRentalApi.enums.Role),
        ),
    ]
