# Generated by Django 4.1.2 on 2022-11-04 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passManagerApp', '0010_alter_card_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='card',
            name='key',
            field=models.CharField(max_length=400),
        ),
    ]
