from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from goods.models import Basket, Category, Product
from goods.permission import IsOwner
from goods.serializers import BasketSerializer, CategorySerializer, ProductSerializer
from goods.services import ProductFilter


# Create your views here.


class ProductPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "prev": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "result": data,
            }
        )


@extend_schema(tags=["Product"])
class ProductListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="add-to-basket",
    )
    def add_to_basket(self, request, *args, **kwargs):
        product = self.get_object()
        user = self.request.user
        quantity = self.request.query_params.get("quantity", 1)
        Basket.objects.create(user=user, product=product, quantity=quantity)
        return Response({"status": "product add to basket"})


@extend_schema(tags=["category"])
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # Выводим категории, которые используются
    queryset = Category.objects.annotate(one=Count("a_category")).filter(one__gt=0)
    serializer_class = CategorySerializer


@extend_schema(tags=["basket"])
class BasketViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BasketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_sum = queryset.total_sum()
        data = {
            "total_sum": total_sum,
            "baskets": self.serializer_class(queryset, many=True, context={"request": request}).data,
        }

        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
