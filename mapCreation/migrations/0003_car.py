# Generated by Django 5.0.6 on 2024-07-11 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapCreation', '0002_endpointusage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_x', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car_y', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car_angle', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
    ]
