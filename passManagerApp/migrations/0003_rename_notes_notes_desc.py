# Generated by Django 4.1.2 on 2022-11-01 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passManagerApp', '0002_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notes',
            old_name='notes',
            new_name='desc',
        ),
    ]
