# Generated by Django 3.0.8 on 2022-02-24 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0019_auto_20220224_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inward',
            options={'ordering': ['company', 'company_goods', 'goods_company', 'agent']},
        ),
        migrations.AlterModelOptions(
            name='outward',
            options={'ordering': ['DC_number']},
        ),
    ]
