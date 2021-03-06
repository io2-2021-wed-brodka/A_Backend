# Generated by Django 3.1.7 on 2021-05-20 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BikeRentalApi', '0005_malfunction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('expire_date', models.DateTimeField()),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BikeRentalApi.bike')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BikeRentalApi.person')),
            ],
        ),
    ]
