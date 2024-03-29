# Generated by Django 4.1.5 on 2023-05-31 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_alter_goods_company_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='company_goods',
            unique_together={('company', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='goods_company',
            unique_together={('company_name', 'company_goods', 'goods_company_name')},
        ),
    ]
