from rest_framework import serializers
from .models import LoyaltyPoints, LoyaltyTransaction

class LoyaltyPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyPoints
        fields = ['user', 'points', 'last_updated']
        
class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyTransaction
        fields = ['user', 'points', 'transaction_type', 'created_at']