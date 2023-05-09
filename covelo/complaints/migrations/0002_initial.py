# Generated by Django 4.1.7 on 2023-05-11 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('complaints', '0001_initial'),
        ('rentals', '0001_initial'),
        ('bicycles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalcomplaint',
            name='rental',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='rental_complaint', to='rentals.rental'),
        ),
        migrations.AddField(
            model_name='bicyclecomplaint',
            name='bicycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bicycle_complaint', to='bicycles.bicycle'),
        ),
    ]
