from django.db.models import fields
from rest_framework import serializers
from .models import *

class usersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = '__all__'
        
class limit_ordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = limit_orders
        fields = '__all__'


class current_market_orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = current_market_order
        fields = '__all__'
        
class trade_historySerializer(serializers.ModelSerializer):
    class Meta:
        model = trade_history
        fields = '__all__'

