# Generated by Django 3.2.5 on 2021-08-16 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='timestamp',
            new_name='time',
        ),
    ]
