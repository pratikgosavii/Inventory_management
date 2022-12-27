# Generated by Django 3.2.15 on 2022-12-21 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_transport'),
        ('transactions', '0022_auto_20220301_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='inward',
            name='LR_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='inward',
            name='freight',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='inward',
            name='transport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sdsxc', to='store.transport'),
        ),
        migrations.AddField(
            model_name='outward',
            name='LR_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='outward',
            name='freight',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='outward',
            name='transport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ddssszc', to='store.transport'),
        ),
        migrations.AddField(
            model_name='supply_return',
            name='LR_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='supply_return',
            name='freight',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='supply_return',
            name='transport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scxsesdf', to='store.transport'),
        ),
    ]
