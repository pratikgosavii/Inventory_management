# Generated by Django 3.2.15 on 2022-12-26 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0023_auto_20221221_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inward',
            name='freight',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]