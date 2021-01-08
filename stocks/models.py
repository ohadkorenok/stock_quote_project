from django.db import models
import uuid


class Stock(models.Model):
    stock_uuid = models.UUIDField(primary_key=True, unique=True, max_length=128, default=uuid.uuid4)
    symbol = models.CharField(max_length=128, null=False, blank=False, db_index=True, unique=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    exchange = models.CharField(max_length=128, null=False, blank=False)
    short_name = models.CharField(max_length=128, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    currency = models.CharField(max_length=20, null=False, blank=False)
    change_percent = models.FloatField(null=False, blank=False)
    avg_daily_volume_10day = models.IntegerField(null=False, blank=False)
    trading_hours = models.BooleanField(null=False, blank=False, default=True)


class PaymentTrack(models.Model):
    number_of_upstream_queries = models.BigIntegerField(default=0)
    query_cost = models.FloatField(default=0.1)
