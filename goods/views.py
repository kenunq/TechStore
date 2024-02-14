from rest_framework.viewsets import ModelViewSet

from goods.models import Product
from goods.serializers import ProductSerializer


# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer