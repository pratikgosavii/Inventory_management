# Generated by Django 3.0.8 on 2022-02-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0018_auto_20220224_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outward',
            name='DC_number',
            field=models.CharField(max_length=566),
        ),
    ]