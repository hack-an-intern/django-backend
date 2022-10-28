from email.policy import default
from django.db import models

# Create your models here.


class users(models.Model):
    name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    fiat = models.IntegerField(default=0)
    stocks = models.IntegerField(default=0)


class limit_orders(models.Model):
    TYPE = (('buy', 'buy'), ('sell', 'sell'))

    type = models.CharField(max_length=50, choices=TYPE, default='buy')
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)


class current_market_order(models.Model):
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)


class trade_history(models.Model):
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    buyer = models.ForeignKey(
        users, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(
        users, on_delete=models.CASCADE, related_name='seller')
