# Generated by Django 3.0.8 on 2020-07-17 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='users',
            new_name='user',
        ),
    ]
