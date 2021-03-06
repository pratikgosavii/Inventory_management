# Generated by Django 3.0.8 on 2022-01-11 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20220110_2342'),
        ('transactions', '0012_remove_stock_agent'),
    ]

    operations = [
        migrations.CreateModel(
            name='supply_return',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bags', models.IntegerField()),
                ('DC_number', models.CharField(max_length=566)),
                ('DC_date', models.DateTimeField()),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fgrrt', to='store.agent')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='we', to='store.company')),
                ('company_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tr', to='store.company_goods')),
                ('goods_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wegvge', to='store.goods_company')),
            ],
        ),
    ]
