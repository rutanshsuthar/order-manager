# orders/serializers.py
from rest_framework import serializers

from .models import Order, OrderItem


class CustomerNameField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_name = CustomerNameField(read_only=True, source='customer')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.customer = validated_data.get('customer', instance.customer)
        instance.save()

        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                item = OrderItem.objects.get(id=item_id, order=instance)
                item.product = item_data.get('product', item.product)
                item.quantity = item_data.get('quantity', item.quantity)
                item.save()
            else:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
