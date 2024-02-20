from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from goods.models import Product, Category, ProductImage, ProductFeature, Feature, Basket


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]



class ProductFeatureSerializer(serializers.ModelSerializer):
    feature = serializers.CharField(source="feature.name")
    class Meta:
        model = ProductFeature
        fields = ['feature', 'value']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    images = ProductImagesSerializer(many=True)
    features = serializers.SerializerMethodField('get_features')

    @extend_schema_field({'example': [{'future': 'name', 'value': 'value'}, {'future': 'name', 'value': 'value'}]})
    def get_features(self, obj):
        return ProductFeatureSerializer(ProductFeature.objects.filter(product_id=obj.id), many=True).data

    class Meta:
        model = Product
        exclude = ['is_published']


class BasketSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()
    total_sum = serializers.SerializerMethodField('get_total_sum')

    @extend_schema_field({'example': '14.44'})
    def get_total_sum(self, obj):
        return obj.product.price * obj.quantity
    class Meta:
        model = Basket
        exclude = ['user']
