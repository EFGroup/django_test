# Generated by Django 4.1.3 on 2023-01-01 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_apikey'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='APIKey',
            new_name='UserAPIKey',
        ),
    ]
