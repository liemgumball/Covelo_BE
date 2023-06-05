# Generated by Django 4.1.7 on 2023-06-04 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FCMToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcm_token', models.CharField(max_length=100, null=True, unique=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fcm_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
