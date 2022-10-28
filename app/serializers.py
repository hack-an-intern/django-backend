from django.db.models import fields
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LimitOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitOrder
        fields = '__all__'


class CurrentMarketOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentMarketOrder
        fields = '__all__'


class TradeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeHistory
        fields = '__all__'
