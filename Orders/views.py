import simplejson as json

from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework import permissions
from rest_framework.response import Response

from Orders.models import Order, UserInfo
from Orders.serializer import OrderSerializer, UserInfoSerializer
from goods.models import Basket
from goods.serializers import BasketSerializer


# Create your views here.


@extend_schema(tags=["Order"])
class OrderListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['status', 'order_price']
    search_fields = ['status']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@extend_schema(tags=['UserInfo'])
class UserInfoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user_info = serializer.save(user=user)
        basket = Basket.objects.filter(user=user)
        basket_ser = BasketSerializer(basket, many=True, context={'request': self.request})
        order_price = basket.total_sum()
        status = 2

        basket_json = json.dumps(basket_ser.data, use_decimal=True, ensure_ascii=False, encoding="utf-8")
        Order.objects.create(user=user, user_info=user_info, basket=basket_json, status=status, order_price=order_price)
        basket.delete()

