# Generated by Django 4.1.5 on 2023-04-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_transport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods_company',
            name='goods_company_name',
            field=models.CharField(max_length=121),
        ),
    ]
