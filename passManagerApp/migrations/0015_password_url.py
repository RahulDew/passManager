# Generated by Django 4.1.2 on 2022-11-23 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passManagerApp', '0014_note_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='password',
            name='url',
            field=models.CharField(default='url', max_length=300),
        ),
    ]
