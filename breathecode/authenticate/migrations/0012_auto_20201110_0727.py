# Generated by Django 3.1.3 on 2020-11-10 07:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0011_credentialsfacebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='github_username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin_url',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AddField(
            model_name='profile',
            name='portfolio_url',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]