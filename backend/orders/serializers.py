from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):  # ✅ Use ModelSerializer
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):  # ✅ Use ModelSerializer
    items = OrderItemSerializer(many=True)  # ✅ Allow creating items

    class Meta:
        model = Order
        fields = ['id',  'status', 'items', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])  # Extract order items
        order = Order.objects.create(**validated_data)  # Create Order

        # ✅ Ensure "quantity" and "price" are set properly
        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order
