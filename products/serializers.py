# products/serializers.py
from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'is_active', 'children']

    def get_children(self, obj):
        children = Category.objects.filter(parent=obj, is_active=True)
        return CategorySerializer(children, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock', 'category', 'is_active']
