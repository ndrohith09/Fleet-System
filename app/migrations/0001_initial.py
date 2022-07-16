# Generated by Django 3.2.11 on 2022-07-16 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=256, primary_key=True, serialize=False, unique=True)),
                ('activity', models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=256, primary_key=True, serialize=False, unique=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('latitude', models.CharField(blank=True, max_length=50, null=True)),
                ('longitude', models.CharField(blank=True, max_length=50, null=True)),
                ('gate_number', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FleetModel',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=256, primary_key=True, serialize=False, unique=True)),
                ('assetid', models.CharField(editable=False, max_length=10, unique=True)),
                ('assetName', models.CharField(blank=True, max_length=256, null=True)),
                ('numberPlate', models.CharField(blank=True, max_length=256, null=True)),
                ('driverName', models.CharField(blank=True, max_length=256, null=True)),
                ('logs', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
