# Generated by Django 3.0.8 on 2022-01-11 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0013_supply_return'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inward',
            name='DC_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='outward',
            name='DC_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='supply_return',
            name='DC_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
