from django_filters import rest_framework as filters

from goods.models import Product


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()
    category = CharFilterInFilter(field_name='category__name', lookup_expr='in')
    brand = filters.CharFilter()
    class Meta:
        model = Product
        fields = ['price', 'brand', 'category']
