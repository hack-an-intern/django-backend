from rest_framework import serializers
from app.models import users
class usersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ('name', 'email', 'fiat', 'stocks')