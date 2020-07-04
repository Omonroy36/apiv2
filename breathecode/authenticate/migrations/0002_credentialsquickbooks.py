# Generated by Django 3.0.7 on 2020-07-03 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authenticate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsQuickBooks',
            fields=[
                ('quibooks_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('quibooks_realmid', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
