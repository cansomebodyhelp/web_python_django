# Generated by Django 5.1.8 on 2025-04-02 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('platform', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('train_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.CharField(max_length=5)),
                ('arrival_time', models.CharField(max_length=5)),
                ('arrival_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='schedule.station')),
                ('departure_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='schedule.station')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.train')),
            ],
        ),
    ]
