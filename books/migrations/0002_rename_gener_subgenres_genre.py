# Generated by Django 4.2.7 on 2023-12-12 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subgenres',
            old_name='gener',
            new_name='genre',
        ),
    ]
