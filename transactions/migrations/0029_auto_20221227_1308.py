# Generated by Django 3.2.15 on 2022-12-27 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0028_auto_20221227_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inward',
            name='DC_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='outward',
            name='DC_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='supply_return',
            name='DC_date',
            field=models.DateTimeField(),
        ),
    ]
