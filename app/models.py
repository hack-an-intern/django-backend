from email.policy import default
from django.db import models

# Create your models here.


class User(models.Model):
    name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    fiat = models.FloatField(default=0)
    stocks = models.FloatField(default=0)

    def __str__(self):
        return self.name

class LimitOrder(models.Model):
    TYPE = (('buy', 'buy'), ('sell', 'sell'))

    type = models.CharField(max_length=50, choices=TYPE, default='buy')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.name} {self.type} {self.quantity} stocks at {self.price}'


class CurrentMarketPrice(models.Model):
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.price} at time {self.time}'
    

class TradeHistory(models.Model):

    TYPE = (('buy', 'buy'), ('sell', 'sell'))

    type = models.CharField(max_length=50, choices=TYPE, default='buy')
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    user1 = models.ForeignKey(                      # buyer
        User, on_delete=models.CASCADE, related_name='buyer')
    user2 = models.ForeignKey(                      # seller
        User, on_delete=models.CASCADE, related_name='seller')
    
    def __str__(self):
        return f'{self.user1.name} {self.type} {self.quantity} stocks at {self.price} from {self.user2.name}'
