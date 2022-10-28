from email.policy import default
from django.db import models

# Create your models here.


class User(models.Model):
    name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    fiat = models.FloatField(default=0)
    stocks = models.FloatField(default=0)


class LimitOrder(models.Model):
    TYPE = (('buy', 'buy'), ('sell', 'sell'))

    type = models.CharField(max_length=50, choices=TYPE, default='buy')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)


class CurrentMarketOrder(models.Model):
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)


class TradeHistory(models.Model):
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='seller')
