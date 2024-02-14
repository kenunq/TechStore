from rest_framework import serializers

from goods.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'old_price', 'category', 'brand', 'available_quantity', 'features']
        depth = 1
