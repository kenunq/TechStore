from rest_framework import serializers

from goods.models import Product, Category, ProductImage, ProductFeature, Feature


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


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    images = ProductImagesSerializer(many=True)
    features = serializers.SerializerMethodField('get_features')

    def get_features(self, obj):
        return ProductFeatureSerializer(ProductFeature.objects.filter(product_id=obj.id), many=True).data

    class Meta:
        model = Product
        exclude = ['is_published']
