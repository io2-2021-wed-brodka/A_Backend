# Generated by Django 3.1.7 on 2021-04-11 20:00

import BikeRentalApi.enums
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('BikeRentalApi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='BikeRentalApi.person')),
            ],
            bases=('BikeRentalApi.person',),
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='BikeRentalApi.person')),
                ('state', django_enumfield.db.fields.EnumField(default=0, enum=BikeRentalApi.enums.UserState)),
            ],
            bases=('BikeRentalApi.person',),
        ),
        migrations.CreateModel(
            name='Tech',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='BikeRentalApi.person')),
            ],
            bases=('BikeRentalApi.person',),
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BikeRentalApi.bike')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BikeRentalApi.appuser')),
            ],
        ),
    ]
