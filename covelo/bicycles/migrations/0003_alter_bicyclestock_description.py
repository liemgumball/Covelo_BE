# Generated by Django 4.1.7 on 2023-05-08 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bicycles', '0002_bicyclestock_bicycle_magnetic_key_bicycle_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bicyclestock',
            name='description',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
