# Generated by Django 4.1.2 on 2022-11-04 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passManagerApp', '0007_alter_card_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiry_date',
            field=models.DateField(),
        ),
    ]