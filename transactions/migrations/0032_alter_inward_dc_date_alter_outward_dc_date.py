# Generated by Django 4.1.5 on 2023-05-26 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0031_alter_supply_return_dc_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inward',
            name='DC_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='outward',
            name='DC_date',
            field=models.DateField(),
        ),
    ]