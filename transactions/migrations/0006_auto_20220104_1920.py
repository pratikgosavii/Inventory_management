# Generated by Django 3.0.8 on 2022-01-04 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='bags',
            new_name='total_bag',
        ),
    ]
