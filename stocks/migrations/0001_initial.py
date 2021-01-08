# Generated by Django 3.1.5 on 2021-01-08 18:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_upstream_queries', models.BigIntegerField(default=0)),
                ('query_cost', models.FloatField(default=0.1)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stock_uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('symbol', models.CharField(db_index=True, max_length=128, unique=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('exchange', models.CharField(max_length=128)),
                ('short_name', models.CharField(max_length=128)),
                ('price', models.FloatField()),
                ('currency', models.CharField(max_length=20)),
                ('change_percent', models.FloatField()),
                ('avg_daily_volume_10day', models.IntegerField()),
                ('trading_hours', models.BooleanField(default=True)),
            ],
        ),
    ]
