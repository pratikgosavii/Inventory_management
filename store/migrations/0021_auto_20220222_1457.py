# Generated by Django 3.0.8 on 2022-02-22 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20220115_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company_goods',
            name='bag_size',
        ),
        migrations.RemoveField(
            model_name='company_goods',
            name='pck_size',
        ),
    ]
