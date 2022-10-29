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

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(LimitOrderSerializer, self).to_representation(instance)


class CurrentMarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentMarketPrice
        fields = '__all__'


class TradeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeHistory
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['user1'] = UserSerializer(read_only=True)
        self.fields['user2'] = UserSerializer(read_only=True)
        return super(TradeHistorySerializer, self).to_representation(instance)
