# Generated by Django 4.1.2 on 2022-11-21 07:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('passManagerApp', '0011_alter_card_card_number_alter_card_expiry_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='creat_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
